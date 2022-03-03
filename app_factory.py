"""App factory to prevent circular dependency"""

import os
import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = "c79ddace-ece1-4358-8b72-de8c0117d9ea"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_ALT")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
