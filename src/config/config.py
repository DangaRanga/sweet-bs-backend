"""For configuring the application."""
# Standard imports
import os

# Flask imports
from flask import Flask


class FlaskApp(Flask):
    """Primary class for the flask application."""

    def __init__(self, import_name):
        """Initialize the Flask App."""
        # Inherit class methods and attributes from super class
        super(FlaskApp, self).__init__(import_name)

        # Update Configuration values
        self.config.update(
            SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            JWT_ACCESS_LIFESPAN=os.environ.get("ACCESS_LIFESPAN"),
            JWT_REFRESH_LIFESPAN=os.environ.get("REFRESH_LIFESPAN"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("DB_URI")
        )
