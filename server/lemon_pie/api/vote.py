import logging
from typing import Dict, Union

from flask import Blueprint, request
from flask_login import current_user, login_required
from lemon_pie import controller
from lemon_pie.controller import AggVote
from lemon_pie.storage.storage import get_storage
from werkzeug.exceptions import BadRequest

from .error import ErrorResponse, error_response

app = Blueprint('votes', __name__, url_prefix="/api")


@app.route('/votes')
@login_required
def get_votes() -> Dict[str, AggVote]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"getting votes for {current_user.key}")
    return controller.get_votes(storage)


@app.route('/users/<user>/votes')
@login_required
def get_user_votes(user) -> Dict[str, AggVote]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"getting votes for {current_user.key}")
    return controller.get_votes(storage, user)


@app.route('/votes', methods=["PUT"])
@login_required
def put_vote() -> Union[Dict[str, AggVote], ErrorResponse]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"user is voting: {current_user.key}")

    try:
        vote_dict = request.get_json()
        if vote_dict is None or type(vote_dict) != dict:
            raise ValueError("invalid request body")

        vote_dict["src"] = {"key": current_user.key}
        response = controller.put_vote(storage, vote_dict)
    except (BadRequest, ValueError) as e:
        return error_response(str(e), 400)

    return response
