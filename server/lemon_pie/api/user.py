import logging
from typing import Callable, Dict, List

from flask import Blueprint
from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage

from .login_utils import login_required

app = Blueprint('users', __name__, url_prefix="/api")


@app.route('/users', methods=["GET"])
@login_required
def get_users(current_user: Callable) -> Dict[str, List[User]]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"user is getting users: {current_user()}")
    return {"users": storage.select_users()}


@app.route('/me', methods=["GET"])
@login_required
def get_me(current_user: Callable) -> Dict[str, str]:
    return {"key": current_user()}
