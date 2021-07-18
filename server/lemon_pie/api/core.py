import os
from lemon_pie import constants
from typing import Optional

from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager

from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage
from . import user, vote, login, emoji

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


def init(env: str):
    app.secret_key = (
        os.environ["SECRET_KEY"]
        if env == constants.PRODUCTION
        else os.environ.get("SECRET_KEY", "development-secret")
    )

    app.config['SESSION_COOKIE_SAMESITE'] = "None"
    app.config['SESSION_COOKIE_SECURE'] = "True"

    origins = ["https://localhost:3000"]
    CORS(app, supports_credentials=True, origins=origins)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    storage = get_storage()
    return storage.select_user(user_id)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def get_ui(path: str) -> str:
    return render_template('index.html')
