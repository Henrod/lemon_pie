from google.auth.transport import requests
from google.oauth2 import id_token
from lemon_pie.models.user import User
from lemon_pie.storage.storage import Storage


def login(
    storage: Storage,
    token: str,
    google_client_id: str,
) -> User:
    idinfo = id_token.verify_oauth2_token(
        token, requests.Request(),
        google_client_id)

    user_id = idinfo["sub"]
    user_email = idinfo["email"]
    user_name = idinfo["given_name"]
    user_surname = idinfo["family_name"]

    user = storage.select_user(user_email=user_email)
    if user is None:
        raise ValueError(f"""user not found in storage:
        id={user_id}, name={user_name}, email={user_email}""")

    user = User(key=f"{user_name}.{user_surname}".lower(),
                id=user_id,
                name=user_name,
                email=user_email)

    storage.update_user(user)

    return user
