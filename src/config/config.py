"""For configuring the application."""

# Standard imports
import os
from dotenv import load_dotenv

# Flask imports


class Config():
    """Primary class for configuration."""

    if (os.path.isfile('.env') is True):
        load_dotenv(".env")

    # Flask Config
    FLASK_ENV = os.environ.get('FLASK_ENV')
    
    FLASK_ADMIN_SWATCH = 'cerulean'

    # JWT Config
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}

    BCRYPT_LOG_ROUNDS = 15

    # SQL Alchemy config
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security config
    CSRF_ENABLED = True

    SESSION_TYPE= os.environ.get("SESSION_TYPE")
    SECRET_KEY=os.environ.get("SECRET_KEY")


    def __init__(self, debug_mode=True):
        """Initialize class."""
        self.debug_mode = debug_mode

app_config = {
    'development': Config(),
    'production': Config(False)
}
