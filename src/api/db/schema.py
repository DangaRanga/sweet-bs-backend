"""Defines the database classes."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the SQLAlchemy object
db = SQLAlchemy()


class User(db.Model):
    """Database model for a User."""

    __tablename__ = 'users'

    def __init__(self, email, password, name):
        self.email = email
        self.password = self.set_password(password)
        self.name = name

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Authentication fields
    username = db.Column(
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

    firstname = db.Column(
        db.String(100),
        primary_key=False,
        unique=False,
        nullable=False
    )

    lastname = db.Column(
        db.String(100),
        primary_key=False,
        unique=False,
        nullable=False
    )

    address = db.Column(
        db.String(225)
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

    items = relationship("OrderItem", cascade="all, delete")


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50)
    )


menuitems_ingredients = db.Table('menuitems_ingredients', db.Model.metadata, db.Column(
    'menuitem_id', db.Integer, db.ForeignKey('menuitems.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id')))


class MenuItem(db.Model):

    __tablename__ = 'menuitems'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        unique=True
    )

    price = db.Column(
        db.Numeric(10, 2)
    )

    description = db.Column(
        db.String(225)
    )

    imageUrl = db.Column(
        db.String(225)
    )

    ingredients = relationship("Ingredient", secondary=menuitems_ingredients)

    orderitems = relationship("OrderItem", cascade="all, delete")


class OrderItem(db.Model):

    __tablename__ = 'orderitems'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    qty = db.Column(
        db.Integer
    )

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    menuitem_id = db.Column(db.Integer, db.ForeignKey("menuitems.id"))
