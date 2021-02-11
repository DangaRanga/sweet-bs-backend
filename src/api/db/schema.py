"""Defines the database classes."""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the SQLAlchemy object
db = SQLAlchemy()


class User(db.Model):
    """Database model for a User."""

    __tablename__ = 'user'

    def __init__(self, email, password, name):
        self.email = email
        self.password = self.set_password(password)
        self.name = name

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Authentication fields
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    # Fields for JWT
    public_id = db.Column(
        db.String(50),
        unique=True
    )

    created_on = db.Column(     # To easily allow for users to be deleted based on their date
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    # Class methods

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    complete = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )


class Ingredient():
    pass


class MenuItem():
    pass
