from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Emoji:
    key: str
    value: str
    create_time: date = None
    update_time: date = None
