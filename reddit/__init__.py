from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from reddit.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"


def create_app(config=Config):
    """
    Factory method for creating the reddit flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)

    from reddit.auth import auth_blueprint
    from reddit.communities import communities_blueprint
    from reddit.community import community_blueprint
    from reddit.feed import feed_blueprint
    from reddit.post import post_blueprint
    from reddit.reply import reply_blueprint
    from reddit.user import user_blueprint
    from reddit.cli import cli_app_group

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(communities_blueprint)
    app.register_blueprint(community_blueprint)
    app.register_blueprint(feed_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(reply_blueprint)
    app.register_blueprint(user_blueprint)
    app.cli.add_command(cli_app_group)

    return app
