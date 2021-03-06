from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional, Set, Tuple

from lemon_pie.models.user import User
from lemon_pie.models.vote import Vote
from lemon_pie.storage.storage import Storage

from .dataclasses import AggVote, Votes


def _get_today(start_vote_time: time) -> date:
    now = datetime.utcnow()
    today = now.date()

    if now.time() < start_vote_time:
        return today - timedelta(days=1)

    return today


def _to_timezone(t: time) -> time:
    # TODO: use timezone better
    tz = - timedelta(hours=3)
    dummy_date = datetime(100, 1, 1, t.hour, t.minute, t.second)
    return (dummy_date + tz).time()


def can_vote(start_vote_time: time, end_vote_time: time) -> bool:
    now = datetime.utcnow().time()
    if start_vote_time < end_vote_time:
        return start_vote_time < now < end_vote_time
    else:
        return start_vote_time < now or now < end_vote_time


def is_vote_opened(storage: Storage) -> bool:
    return bool(storage.select_configs().is_vote_opened)


def _valid_users(
    users: List[User],
    votes: List[Vote],
) -> Set[User]:
    valid_src_users: Set[User] = set()

    users_set = set(User(key=user.key) for user in users)
    for user in users:
        user_votes = set(vote.dst for vote in votes if vote.src == user)
        if user_votes.issuperset(users_set - {user}):
            valid_src_users.add(user)

    return valid_src_users


def _get_agg_votes(
    users: List[User],
    votes: List[Vote],
    src_key: str = None,
) -> Dict[str, AggVote]:
    valid_src_users = _valid_users(users, votes)

    agg_votes: Dict[str, AggVote] = {
        user.key: AggVote.new(
            User(key=user.key, name=user.name),
            is_counting=(user in valid_src_users)
        ) for user in users if src_key != user.key
    }

    for vote in votes:
        is_valid_src = src_key is None and vote.src in valid_src_users
        is_vote_src = src_key == vote.src.key
        is_valid_dst = vote.dst.key in agg_votes
        if (is_valid_src or is_vote_src) and is_valid_dst:
            agg_votes[vote.dst.key].votes[vote.key].count += 1

    return agg_votes


def _get_users_date(users: List[User]) -> Dict[date, List[User]]:
    users_date: Dict[date, List[User]] = {}
    for user in users:
        if user.create_time is None:
            raise RuntimeError("user.create_time must not be None")

        key = user.create_time.date()
        users_date[key] = users_date.get(key, [])
        users_date[key].append(user)

    return users_date


def get_votes(
    storage: Storage,
    start_vote_time: time,
    end_vote_time: time,
    should_total: bool = False,
    src_key: str = None,
) -> Dict:
    if should_total:
        votes: Dict[date, List[Vote]] = {}
        for vote in storage.select_votes():
            votes[vote.date] = votes.get(vote.date, [])
            votes[vote.date].append(vote)

        start_date = min(d for d in votes.keys())
        end_date = max(d for d in votes.keys())
    else:
        today = _get_today(start_vote_time)
        votes = {today: storage.select_votes_date(today)}
        start_date, end_date = today, today

    users_date = _get_users_date(storage.select_users())
    total_agg_votes: Dict[str, AggVote] = {
        user.key: AggVote.new(
            User(key=user.key, name=user.name),
            is_counting=False,
        )
        for users in users_date.values()
        for user in users
        if src_key != user.key
    }

    for vote_date, votes_date in votes.items():
        vs = sorted(votes_date, key=lambda vote: vote.key)
        users = [
            user
            for create_date, users in users_date.items()
            for user in users
            if create_date <= vote_date
        ]

        agg_votes = _get_agg_votes(users, vs, src_key)
        for user_key, user_agg_votes in agg_votes.items():
            total_agg_votes[user_key] += user_agg_votes

    votes_dict = Votes(
        start_date=start_date,
        end_date=end_date,
        votes=total_agg_votes,
        can_vote=(
            can_vote(start_vote_time, end_vote_time) and
            is_vote_opened(storage)
        ),
    ).to_dict()

    vote_starts_at, vote_ends_at = get_vote_times(
        storage,
        start_vote_time, end_vote_time)

    return {
        **votes_dict,
        "times": {
            "starts_at": vote_starts_at,
            "ends_at": vote_ends_at,
        }
    }


def _is_invalid(cases: List[Tuple[bool, str]]) -> Optional[str]:
    for is_valid, error_msg in cases:
        if not is_valid:
            return error_msg
    return None


def put_vote(
    storage: Storage,
    start_vote_time: time,
    end_vote_time: time,
    vote_dict: dict,
) -> Dict[str, AggVote]:
    logger = logging.getLogger(__name__)

    src_user_key = vote_dict.get("src", {}).get("key")
    dst_user_key = vote_dict.get("dst", {}).get("key")
    vote_key = vote_dict.get("key", "")
    today = _get_today(start_vote_time)

    vote = Vote(
        src=User(key=src_user_key),
        dst=User(key=dst_user_key),
        key=vote_key,
        date=today,
    )

    valid_users: List[str] = [user.key for user in storage.select_users()]
    valid_emojis: List[str] = [emoji.key for emoji in storage.select_emojis()]

    error_msg = _is_invalid([
        (vote.src.key in valid_users, "not a valid source user"),
        (vote.dst.key in valid_users, "not a valid target user"),
        (vote.key in valid_emojis, "not a valid vote"),
        (vote.src.key != vote.dst.key, "source user cannot be target one"),
    ])
    if error_msg:
        logger.warning(f"invalid vote: {vote} - {error_msg}")
        raise ValueError(error_msg)

    storage.delete_vote((vote.date, vote.src.key, vote.dst.key))
    storage.insert_vote(vote)

    return get_votes(
        storage=storage,
        start_vote_time=start_vote_time,
        end_vote_time=end_vote_time,
        src_key=vote.src,
    )


def is_total_enabled(
    storage: Storage,
    user_key: str,
) -> bool:
    configs = storage.select_configs()
    if configs.is_total_enabled:
        return True

    user = storage.select_user(user_key=user_key)
    if user.key and user.is_admin:
        return True

    return False


def get_vote_times(
    storage: Storage,
    start_vote_time: time,
    end_vote_time: time,
) -> Tuple[Optional[str], Optional[str]]:
    vote_starts_at: Optional[time] = None
    vote_ends_at: Optional[time] = None

    if is_vote_opened(storage):
        if can_vote(start_vote_time, end_vote_time):
            vote_ends_at = end_vote_time
        else:
            vote_starts_at = start_vote_time

    def to_str(t: Optional[time]) -> Optional[str]:
        return None if t is None else _to_timezone(t).strftime("%H:%M")

    return to_str(vote_starts_at), to_str(vote_ends_at)
