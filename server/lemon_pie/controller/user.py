from typing import List

from lemon_pie.models.user import User
from lemon_pie.storage.storage import Storage


def get_users(storage: Storage) -> List[User]:
    users = storage.select_users()
    return [User(key=user.key, name=user.name) for user in users]
