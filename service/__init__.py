"""Flask app for the accounts service."""
import os
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///accounts.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

# Security headers (HSTS, CSP, X-Frame-Options, ...) and CORS
talisman = Talisman(app, force_https=os.getenv("FORCE_HTTPS", "true") == "true")
CORS(app)

from service.models import db  # noqa: E402
from service import routes  # noqa: E402,F401

db.init_app(app)
with app.app_context():
    db.create_all()
