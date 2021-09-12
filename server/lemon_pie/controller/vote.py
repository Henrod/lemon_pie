from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional, Set, Tuple

from lemon_pie.models.user import User
from lemon_pie.models.vote import Vote
from lemon_pie.storage.storage import Storage

from .dataclasses import AggVote, Votes


def _get_today() -> date:
    # TODO: use timezone better
    return (datetime.now() - timedelta(hours=3)).date()


def can_vote(start_vote_time: time, end_vote_time: time) -> bool:
    return start_vote_time < datetime.now().time() < end_vote_time


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
        today = _get_today()
        votes = {today: storage.select_votes_date(today)}
        start_date, end_date = today, today

    users = storage.select_users()
    total_agg_votes: Dict[str, AggVote] = {
        user.key: AggVote.new(
            User(key=user.key, name=user.name),
            is_counting=False,
        ) for user in users if src_key != user.key
    }

    for votes_date in votes.values():
        vs = sorted(votes_date, key=lambda vote: vote.key)
        agg_votes = _get_agg_votes(users, vs, src_key)

        for user_key, user_agg_votes in agg_votes.items():
            total_agg_votes[user_key] += user_agg_votes

    return Votes(
        start_date=start_date,
        end_date=end_date,
        votes=total_agg_votes,
        can_vote=can_vote(start_vote_time, end_vote_time),
    ).to_dict()


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
    today = _get_today()

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
