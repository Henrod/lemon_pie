import logging
import os
from typing import Dict, Union

from flask import Blueprint, request
from flask_login import login_user
from lemon_pie import controller
from lemon_pie.storage.storage import get_storage

from .error import ErrorResponse, error_response

app = Blueprint('login', __name__, url_prefix="/api")

GOOGLE_CLIENT_ID = os.environ["LEMON_PIE_GOOGLE_CLIENT_ID"]


@app.route('/login/callback', methods=["POST"])
def login() -> Union[Dict[str, str], ErrorResponse]:
    logger = logging.getLogger(__name__)
    storage = get_storage()

    token = request.headers.get("Authorization")
    if token is None:
        return error_response("missing Authorization HTTP header", 400)

    try:
        user = controller.login(storage, token, GOOGLE_CLIENT_ID)
    except ValueError as e:
        logger.warning(f'failed to login: {str(e)}')
        return error_response("user not registared in storage", 403)

    login_user(user)
    return {"key": user.key}
