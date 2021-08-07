from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Tuple

from lemon_pie.models import Emoji, User, Vote, Configs


class Storage(ABC):
    @abstractmethod
    def select_votes(self) -> List[Vote]:
        pass

    @abstractmethod
    def select_votes_date(self, date: date) -> List[Vote]:
        pass

    @abstractmethod
    def insert_vote(self, vote: Vote) -> None:
        pass

    @abstractmethod
    def delete_vote(self, vote_pk: Tuple[date, str, str]) -> None:
        pass

    @abstractmethod
    def select_users(self) -> List[User]:
        pass

    @abstractmethod
    def select_user(
        self,
        user_id: str = None,
        user_email: str = None,
        user_key: str = None,
    ) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def insert_emoji(self, emoji: Emoji) -> None:
        pass

    @abstractmethod
    def delete_emoji(self, emoji_key: str) -> None:
        pass

    @abstractmethod
    def select_emojis(self) -> List[Emoji]:
        pass

    @abstractmethod
    def select_configs(self) -> Configs:
        pass


_storage: Storage


def init_storage(storage: Storage) -> None:
    global _storage
    _storage = storage


def get_storage() -> Storage:
    global _storage
    return _storage
