from flask import Blueprint

user_blueprint = Blueprint("user", __name__)

from reddit.user import routes
