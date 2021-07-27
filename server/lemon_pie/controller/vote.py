from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from lemon_pie.storage.storage import get_storage
from typing import Dict, List, Optional, Set, Tuple

from lemon_pie.models.user import User
from lemon_pie.models.vote import Vote
from lemon_pie.storage.storage import Storage


@dataclass
class VoteCount:
    value: str
    count: int


@dataclass(frozen=True)
class AggVote:
    user: User
    votes: Dict[str, VoteCount]
    is_counting: bool

    @staticmethod
    def new(user: User, is_counting: bool) -> AggVote:
        return AggVote(
            user=user,
            votes={
                emoji.key: VoteCount(value=emoji.value, count=0)
                for emoji in get_storage().select_emojis()
            },
            is_counting=is_counting,
        )


@dataclass
class Votes:
    votes: Dict[str, AggVote]
    can_vote: bool


def can_vote(end_vote_time: time) -> bool:
    return datetime.now().time() < end_vote_time


def get_votes(
    storage: Storage,
    end_vote_time: time,
    src_key: str = None,
) -> Dict:
    today = date.today()
    users = storage.select_users()

    votes = storage.select_votes(today)
    votes = sorted(votes, key=lambda vote: vote.key)

    valid_src_users: Set[User] = set()
    users_set = set(User(key=user.key) for user in users)
    for user in users:
        user_votes = set(vote.dst for vote in votes if vote.src == user)
        if user_votes == users_set - {user}:
            valid_src_users.add(user)

    agg_votes: Dict[str, AggVote] = {
        user.key: AggVote.new(
            User(key=user.key, name=user.name),
            is_counting=(user in valid_src_users)
        ) for user in users if src_key != user.key
    }

    for vote in votes:
        if (src_key is None and vote.src in valid_src_users) \
                or src_key == vote.src.key:
            agg_votes[vote.dst.key].votes[vote.key].count += 1

    return asdict(Votes(
        votes=agg_votes,
        can_vote=can_vote(end_vote_time),
    ))


def _is_invalid(cases: List[Tuple[bool, str]]) -> Optional[str]:
    for is_valid, error_msg in cases:
        if not is_valid:
            return error_msg
    return None


def put_vote(storage: Storage, vote_dict: dict) -> Dict[str, AggVote]:
    logger = logging.getLogger(__name__)

    src_user_key = vote_dict.get("src", {}).get("key")
    dst_user_key = vote_dict.get("dst", {}).get("key")
    vote_key = vote_dict.get("key", "")
    today = date.today()

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

    return get_votes(storage, vote.src)
