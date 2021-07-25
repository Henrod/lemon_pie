import os
from datetime import time
from typing import Optional

from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from lemon_pie import constants
from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage

from . import emoji, login, login_utils, user, vote

app = Flask(
    __name__,
    static_folder="../build/static",
    template_folder="../build",
)

app.register_blueprint(user.app)
app.register_blueprint(vote.app)
app.register_blueprint(login.app)
app.register_blueprint(emoji.app)

login_manager = LoginManager()
login_manager.init_app(app)


def init(env: str, end_vote_time: time):
    login_utils.init(env)
    vote.init(end_vote_time)

    if env == constants.PRODUCTION:
        origins = os.environ["LEMON_PIE_CORS_ORIGINS"].split(",")
        app.secret_key = os.environ["LEMON_PIE_SECRET_KEY"]
        app.config["SESSION_COOKIE_SAMESITE"] = "None"
        app.config["SESSION_COOKIE_SECURE"] = "True"
    else:
        origins = ["*"]
        app.secret_key = "development-secret"
        app.config["LOGIN_DISABLED"] = True

    CORS(app, supports_credentials=True, origins=origins)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    storage = get_storage()
    return storage.select_user(user_id)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def get_ui(path: str) -> str:
    return render_template("index.html")
