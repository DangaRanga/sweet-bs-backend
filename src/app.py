

from flask import Flask
from config.config import app_config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


class FlaskApp(Flask):

    def __init__(self):
        # Inherit class methods from Flask
        super(FlaskApp, self).__init__("Sweet B's Server")

        # Configure the Flask app
        self.config.from_object(Config)
        self.config.from_object(app_config)

        # Initialize the SQLAlchemy Database
        self.db = SQLAlchemy(self)
        self.ma = Marshmallow(self)
        self.bcrypt = Bcrypt(self)
        

    def db_create_all(self):
        with self.app_context():
            self.db.create_all()
