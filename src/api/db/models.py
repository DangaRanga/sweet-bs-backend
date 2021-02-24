
"""Defines the database classes."""
# SQLAlchemy Imports
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from marshmallow import fields
from sqlalchemy import event, text

# Python imports
from datetime import datetime
import uuid
from enum import unique

# User module imports
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

    # Identification fields: Username, Email, Password
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
        'password',
        app.db.String(128),
        nullable=False,
    )

    # Personal details, name and address
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

    # Authorization fields
    is_admin = app.db.Column(
        app.db.Boolean,
        default=False
    )

    # Fields for JWT
    public_id = app.db.Column(
        app.db.String(50),
        unique=True,
        default=uuid.uuid4
    )

    # To easily allow for users to be deleted based on their date
    created_on = app.db.Column(
        app.db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.now
    )

    _orders_placed = app.db.relationship(
        "OrderModel", cascade="all, delete, delete-orphan", backref="user")

    # Class methods

    @hybrid_property
    def password(self):
        return self._password

    def __repr__(self) -> str:
        return f"{self.firstname} {self.lastname} ({self.username})"

    @password.setter
    def password(self, password):
        """Create hashed password."""

        self._password = app.bcrypt.generate_password_hash(
            password).decode('utf8')  # Decoding so it doesn't get saved as binary

    @hybrid_method
    def check_password(self, password):
        """Check hashed password."""
        return app.bcrypt.check_password_hash(self._password, password)

    @hybrid_property
    def orders_placed(self):
        return len(self._orders_placed)


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


menuitems_ingredients = app.db.Table(
    'menuitems_ingredients', app.db.Model.metadata,
    app.db.Column(
        'menuitem_id', app.db.Integer, app.db.ForeignKey('menuitems.id')),
    app.db.Column(
        'ingredient_id', app.db.Integer, app.db.ForeignKey('ingredients.id')))


class MenuItemCategoryModel(app.db.Model):

    __tablename__ = 'menuitem_categories'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    category = app.db.Column(
        app.db.String(40),
        unique=True,
        nullable=False
    )

    menuitems = app.db.relationship(
        "MenuItemModel",
        cascade="all, delete", backref="category", lazy="joined")

    def __repr__(self) -> str:
        return f"{self.category}"


class MenuItemModel(app.db.Model):

    __tablename__ = 'menuitems'

    id = app.db.Column(
        app.db.Integer,
        primary_key=True
    )

    flavour = app.db.Column(
        app.db.String(50),
        nullable=False
    )

    category_id = app.db.Column(
        app.db.Integer,
        app.db.ForeignKey("menuitem_categories.id"),
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
        "IngredientModel",
        secondary=menuitems_ingredients, backref="related_menuitems")

    orderitems = app.db.relationship(
        "OrderItemModel", cascade="all, delete", backref="menuitem")

    def __repr__(self) -> str:
        return f"{self.flavour} {self.category}"


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
        return f"{self.menuitem} x{self.qty}"


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

    user_id = app.db.Column(
        app.db.Integer, app.db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Order #{self.id}"

    # Ensure that empty orders are deleted
    @staticmethod
    @event.listens_for(OrderItemModel, 'after_delete')
    def delete_empty_order(mapper, connection, target):
        if not target.order.items:
            print("works")
            del_query = f"delete from orders where orders.id={target.order.id}"
            connection.execute(text(del_query))


class IngredientSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientModel


class MenuItemSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemModel

    ingredients = app.ma.Nested(IngredientSchema, default=[], many=True)
    category = fields.String(attribute="category")


class OrderItemSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItemModel
        include_fk = True
        exclude = ("menuitem_id", "order_id")

    menuitem = app.ma.Nested(MenuItemSchema)


class OrderSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        exclude = ("user_id",)

    class OrderUserSchema(app.ma.SQLAlchemyAutoSchema):
        class Meta:
            model = UserModel
            exclude = ("_password",)

    items = app.ma.Nested(OrderItemSchema, default=[], many=True)
    user = app.ma.Nested(OrderUserSchema)


class UserSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ("_password",)

    password = fields.String(attribute='_password')
    orders_placed = fields.Integer(attribute='orders_placed')


class MenuItemCategorySchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemCategoryModel

    menuitems = app.ma.Nested(MenuItemSchema, many=True, default=[])
