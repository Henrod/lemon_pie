from typing import Optional
from lemon_pie.models.user import User
from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class Vote:
    src: User
    dst: User
    key: str
    date: date
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
