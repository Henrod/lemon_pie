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
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
