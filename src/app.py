

from typing import List
from urllib.parse import urlparse
from eventlet.greenthread import GreenThread
from flask import Flask
from config.config import app_config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
import pgpubsub


class FlaskApp(Flask):

    def __init__(self):
        # Inherit class methods from Flask
        super(FlaskApp, self).__init__("Sweet B's Server")

        # Configure the Flask app
        self.config.from_object(Config)
        self.config.from_object(app_config)

        # Initialize the SQLAlchemy Database, Marshmallow, Bycrpt, SocketIO, pgpubsub
        self.db = SQLAlchemy(self)
        self.ma = Marshmallow(self)
        self.bcrypt = Bcrypt(self)
        self.socketio = SocketIO(self, cors_allowed_origins="*")
        # A list to store threads spawned by the server for clean up on exit
        self.socket_threads: List[GreenThread] = []
        # psycopg's connect doesn't work natively with the DB_URI string for some reason hence the parsing
        dburl = urlparse(self.config.get('SQLALCHEMY_DATABASE_URI'))
        self.pubsub_conn_det = {"database": dburl.path[1:],
                                "host": dburl.hostname,
                                "password": dburl.password,
                                "user": dburl.username,
                                "port": dburl.port}

    def db_create_all(self):
        with self.app_context():
            self.db.create_all()
