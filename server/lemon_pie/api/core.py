import os
from typing import Optional

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from lemon_pie.models import User
from lemon_pie.storage.storage import get_storage
from . import user, vote, login, emoji

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

app.register_blueprint(user.app)
app.register_blueprint(vote.app)
app.register_blueprint(login.app)
app.register_blueprint(emoji.app)

login_manager = LoginManager()
login_manager.init_app(app)


def init():
    app.config['SESSION_COOKIE_SAMESITE'] = "None"
    app.config['SESSION_COOKIE_SECURE'] = "True"

    origins = ["https://localhost:3000"]
    CORS(app, supports_credentials=True, origins=origins)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    storage = get_storage()
    return storage.select_user(user_id)
