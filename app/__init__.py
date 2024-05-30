import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.permanent_session_lifetime = timedelta(hours=1)
db = SQLAlchemy(app)

from app import routes
