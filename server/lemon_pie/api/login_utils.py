import functools
import os
from typing import Callable, Optional

import flask_login
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user
from lemon_pie import constants

env: str = ""


def init(app_env: str) -> None:
    global env
    env = app_env


def verify_basic_auth(username: str, password: str) -> Optional[str]:
    return username if password == os.environ["LEMON_PIE_PASSWORD"] else None


def login_required(f: Callable) -> Callable:
    basic_auth = HTTPBasicAuth()
    basic_auth.verify_password(verify_basic_auth)

    @ functools.wraps(f)
    def decorator(*args, **kwargs):
        _f = {
            constants.PRODUCTION: flask_login.login_required(f),
            constants.DEVELOPMENT: basic_auth.login_required(f),
        }[env]
        current_user_func = {
            constants.PRODUCTION: lambda: current_user.key,
            constants.DEVELOPMENT: lambda: basic_auth.current_user(),
        }[env]
        return _f(current_user=current_user_func, *args, **kwargs)

    return decorator
