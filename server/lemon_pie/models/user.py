from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flask_login import UserMixin


@dataclass(frozen=True)
class User(UserMixin):
    key: str
    id: str = ""
    name: str = ""
    email: str = ""
    is_admin: bool = False
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    def __eq__(self, other: UserMixin) -> bool:
        return (
            type(other) == User
            and self.key == other.key
            and super().__eq__(other)
        )

    def __hash__(self) -> int:
        return hash(self.key)
