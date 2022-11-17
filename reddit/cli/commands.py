from reddit import db
from reddit.cli import cli_app_group


@cli_app_group.command("create_db")
def create_db():
    """
    CLI command for generating all database tables from SQLAlchemy models.
    """
    db.create_all()
