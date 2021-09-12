import logging
from datetime import time
from typing import Callable, Dict, Union

from flask import Blueprint, request
from lemon_pie import controller
from lemon_pie.controller import AggVote
from lemon_pie.storage.storage import get_storage
from werkzeug.exceptions import BadRequest

from .error import ErrorResponse, error_response
from .login_utils import login_required

app = Blueprint('votes', __name__, url_prefix="/api")

_end_vote_time = time(hour=12)
_start_vote_time = time(hour=0)


def init(start_vote_time: time, end_vote_time: time) -> None:
    global _end_vote_time, _start_vote_time
    _end_vote_time = end_vote_time
    _start_vote_time = start_vote_time


@app.route('/votes')
@login_required
def get_votes(current_user: Callable) -> Dict:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"getting votes for {current_user()}")

    return controller.get_votes(
        storage=storage,
        start_vote_time=_start_vote_time,
        end_vote_time=_end_vote_time,
    )


@app.route('/total')
@login_required
def get_total(current_user: Callable) -> Dict:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"getting votes for {current_user()}")

    fields = request.args.get("fields", default="").split(",")
    should_votes = "votes" in fields

    is_total_enabled = controller.is_total_enabled(storage, current_user())

    total_votes: Dict = {}
    if should_votes and is_total_enabled:
        total_votes = controller.get_votes(
            storage=storage,
            start_vote_time=_start_vote_time,
            end_vote_time=_end_vote_time,
            should_total=True,
        )

    return {
        "is_enabled": is_total_enabled,
        "total": total_votes,
    }


@app.route('/users/<user>/votes')
@login_required
def get_user_votes(user: str, current_user: Callable) -> Dict[str, AggVote]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"getting votes for {current_user()}")
    return controller.get_votes(
        storage=storage,
        start_vote_time=_start_vote_time,
        end_vote_time=_end_vote_time,
        src_key=user,
    )


@app.route('/votes', methods=["PUT"])
@login_required
def put_vote(
    current_user: Callable,
) -> Union[Dict[str, AggVote], ErrorResponse]:
    storage = get_storage()
    logger = logging.getLogger(__name__)
    logger.info(f"user is voting: {current_user()}")

    try:
        vote_dict = request.get_json()
        if vote_dict is None or type(vote_dict) != dict:
            raise ValueError("invalid request body")

        vote_dict["src"] = {"key": current_user()}
        response = controller.put_vote(
            storage,
            _start_vote_time,
            _end_vote_time,
            vote_dict,
        )
    except (BadRequest, ValueError) as e:
        return error_response(str(e), 400)

    return response
