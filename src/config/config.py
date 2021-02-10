"""For configuring the application."""
# Standard imports
import os

# Flask imports


class Config():
    """Primary class for configuration."""

    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}

    def __init__(self, debug_mode=True):
        """Initialize class."""
        self.debug_mode = debug_mode


app_conig = {
    'development': Config(),
    'production': Config(False)
}
