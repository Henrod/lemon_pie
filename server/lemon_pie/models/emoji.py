from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Emoji:
    key: str
    value: str
    create_time: Optional[date] = None
    update_time: Optional[date] = None
