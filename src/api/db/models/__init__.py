# Python imports
from datetime import datetime

# User module imports
from app import FlaskApp


app = FlaskApp()


class Base(app.db.Model):
    """Base Model for all Database Classes."""
    __abstract__ = True

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    created_on = app.db.Column(
        app.db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.now
    )
