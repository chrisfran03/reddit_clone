from flask import Blueprint

auth_blueprint = Blueprint("auth", __name__)

from reddit.auth import routes
