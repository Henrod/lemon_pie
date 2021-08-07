from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Dict

from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage


@dataclass
class VoteCount:
    value: str
    count: int

    def __add__(self, other: VoteCount) -> VoteCount:
        if self.value != other.value:
            raise ValueError("can not add VoteCount of different values")

        return VoteCount(
            value=self.value,
            count=self.count + other.count,
        )


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

    def __add__(self, other: AggVote) -> AggVote:
        if self.user != other.user:
            raise ValueError("can not sum aggregated votes for "
                             "different users")

        agg_vote = AggVote.new(
            user=self.user,
            is_counting=(self.is_counting or other.is_counting),
        )

        for emoji_key in agg_vote.votes.keys():
            agg_vote.votes[emoji_key] = (
                self.votes[emoji_key] +
                other.votes[emoji_key]
            )

        return agg_vote


@dataclass
class Votes:
    start_date: str
    end_date: str
    votes: Dict[str, AggVote]
    can_vote: bool

    def __init__(
        self,
        start_date: date,
        end_date: date,
        votes: Dict[str, AggVote],
        can_vote: bool,
    ) -> None:
        self.start_date = self._format_date(start_date)
        self.end_date = self._format_date(end_date)
        self.votes = votes
        self.can_vote = can_vote

    def _format_date(self, d: date) -> str:
        return d.strftime(r"%d/%m/%Y")

    def to_dict(self) -> Dict:
        return asdict(self)
