from flask import Blueprint

communities_blueprint = Blueprint("communities", __name__)

from reddit.communities import routes
