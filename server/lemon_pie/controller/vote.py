from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from lemon_pie.storage.storage import get_storage
from typing import Dict, List, Optional, Tuple

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

    @staticmethod
    def new(user: User) -> AggVote:
        return AggVote(
            user=user,
            votes={
                emoji.key: VoteCount(value=emoji.value, count=0)
                for emoji in get_storage().select_emojis()
            },
        )


def get_votes(storage: Storage, src_key: str = None) -> Dict[str, AggVote]:
    today = date.today()
    users = storage.select_users()

    agg_votes: Dict[str, AggVote] = {
        user.key: AggVote.new(User(key=user.key, name=user.name))
        for user in users
        if src_key != user.key
    }

    votes = storage.select_votes(today)
    votes = sorted(votes, key=lambda vote: vote.key)

    for vote in votes:
        if src_key is None or src_key == vote.src.key:
            agg_votes[vote.dst.key].votes[vote.key].count += 1

    return agg_votes


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
