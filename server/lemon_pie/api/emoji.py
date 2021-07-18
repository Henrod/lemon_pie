from typing import List, Dict, Union

from flask import Blueprint, request
from lemon_pie.models import Emoji
from lemon_pie.storage.storage import get_storage

from .error import ErrorResponse, error_response

app = Blueprint('emojis', __name__, url_prefix="/api")


@app.route("/emojis")
def get_emojis() -> Dict[str, List[Emoji]]:
    storage = get_storage()
    emojis = storage.select_emojis()
    emojis = sorted(emojis, key=lambda e: e.key)
    return {"emojis": emojis}


@app.route("/emojis", methods=["POST"])
def insert_emojis() -> Union[Dict[str, List[str]], ErrorResponse]:
    storage = get_storage()
    emoji_dict = request.get_json()
    if not emoji_dict:
        return error_response("request body is empty", 400)

    try:
        emoji = Emoji(
            key=emoji_dict["key"],
            value=emoji_dict["value"])
    except KeyError:
        return error_response("request body must have keys: key, value", 400)

    storage.insert_emoji(emoji)

    return get_emojis()


@app.route("/emojis", methods=["DELETE"])
def delete_emoji() -> Union[Dict[str, List[str]], ErrorResponse]:
    storage = get_storage()
    emoji_dict = request.get_json()
    if not emoji_dict:
        return error_response("request body is empty", 400)

    if "key" not in emoji_dict:
        return error_response("request body must have keys: key", 400)

    emoji_key = emoji_dict["key"]
    storage.delete_emoji(emoji_key)

    return get_emojis()
