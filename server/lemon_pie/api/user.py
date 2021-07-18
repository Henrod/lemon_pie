import logging
from typing import Dict, List

from flask_login import current_user, login_required

from flask import Blueprint
from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage

app = Blueprint('users', __name__, url_prefix="/api")


@app.route('/users', methods=["GET"])
@login_required
def get_users() -> Dict[str, List[User]]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"user is getting users: {current_user.key}")
    return {"users": storage.select_users()}


@app.route('/me', methods=["GET"])
@login_required
def get_me() -> Dict[str, str]:
    return {"key": current_user.key}
