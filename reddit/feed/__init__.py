from flask import Blueprint

feed_blueprint = Blueprint("feed", __name__)

from reddit.feed import routes
