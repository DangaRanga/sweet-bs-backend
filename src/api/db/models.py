
"""Defines the database classes."""
from enum import unique
from sqlalchemy.orm import backref
#from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


from app import FlaskApp

# Initialize the App object
app = FlaskApp()


class UserModel(app.db.Model):
    """Database model for a User."""

    __tablename__ = 'users'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    # Authentication fields
    username = app.db.Column(
        app.db.String(100),
        unique=True,
        nullable=False
    )

    email = app.db.Column(
        app.db.String(120),
        unique=True,
        nullable=False
    )

    _password = app.db.Column(
        "password",
        app.db.String(128),
        nullable=False,
    )

    firstname = app.db.Column(
        app.db.String(100),
        nullable=False
    )

    lastname = app.db.Column(
        app.db.String(100),
        nullable=False
    )

    address = app.db.Column(
        app.db.String(225)
    )

    is_admin = app.db.Column(
        app.db.Boolean,
        default=False
    )

    # Fields for JWT
    public_id = app.db.Column(
        app.db.String(50),
        unique=True,
        default=uuid.uuid4()
    )

    created_on = app.db.Column(     # To easily allow for users to be deleted based on their date
        app.db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.now()
    )

    orders_placed = app.db.relationship(
        "OrderModel", cascade="all, delete, delete-orphan", backref="user")

    @hybrid_property
    def password(self):
        return self._password
    # Class methods

    def __repr__(self) -> str:
        return f"{self.firstname} {self.lastname} ({self.username})"

    @password.setter
    def password(self, password):
        """Create hashed password."""
        self._password = app.bcrypt.generate_password_hash(password)

    @hybrid_method
    def check_password(self, password):
        """Check hashed password."""
        return app.bcrypt.check_password_hash(self._password, password)


class OrderModel(app.db.Model):

    __tablename__ = 'orders'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    complete = app.db.Column(
        app.db.Boolean,
        default=False
    )

    items = app.db.relationship(
        "OrderItemModel", cascade="all, delete", backref="order")

    user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('users.id'),nullable=False)

    def __repr__(self) -> str:
        return f"Order #{self.id}"


class IngredientModel(app.db.Model):
    __tablename__ = 'ingredients'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    name = app.db.Column(
        app.db.String(50),
        unique=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return f"{self.name}"


menuitems_ingredients = app.db.Table('menuitems_ingredients',
                                     app.db.Model.metadata,
                                     app.db.Column(
                                         'menuitem_id', app.db.Integer, app.db.ForeignKey('menuitems.id')),
                                     app.db.Column(
                                         'ingredient_id', app.db.Integer, app.db.ForeignKey('ingredients.id')))


class MenuItemModel(app.db.Model):

    __tablename__ = 'menuitems'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    name = app.db.Column(
        app.db.String(50),
        unique=True,
        nullable=False
    )

    price = app.db.Column(
        app.db.Numeric(10, 2, asdecimal=False),
        nullable=False
    )

    description = app.db.Column(
        app.db.String(225)
    )

    image_url = app.db.Column(
        app.db.String(225)
    )

    ingredients = app.db.relationship(
        "IngredientModel", secondary=menuitems_ingredients, backref="related_menuitems")

    orderitems = app.db.relationship(
        "OrderItemModel", cascade="all, delete", backref="menuitem")

    def __repr__(self) -> str:
        return f"{self.name}"


class OrderItemModel(app.db.Model):

    __tablename__ = 'orderitems'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    qty = app.db.Column(
        app.db.Integer,
        nullable=False
    )

    order_id = app.db.Column(
        app.db.Integer, app.db.ForeignKey("orders.id"), nullable=False)

    menuitem_id = app.db.Column(
        app.db.Integer, app.db.ForeignKey("menuitems.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Menu item #{self.menuitem_id} x{self.qty}"


class IngredientSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientModel


class MenuItemSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemModel

    ingredients = app.ma.Nested(IngredientSchema, default=[], many=True)


class OrderItemSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItemModel
        include_fk = True
        exclude = ("menuitem_id", "order_id")

    menuitem = app.ma.Nested(MenuItemSchema)


class OrderSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        include_fk = True

    class OrderUserSchema(app.ma.SQLAlchemyAutoSchema):
        class Meta:
            model = UserModel

    items = app.ma.Nested(OrderItemSchema, default=[], many=True)
    customer = app.ma.Nested(OrderUserSchema)


class UserSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    orders_placed = app.ma.Nested(
        OrderSchema, default=[], many=True, exclude=["user_id", "customer"])
