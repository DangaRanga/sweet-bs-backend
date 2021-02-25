"""Defines the database Schema."""
# SQLAlchemy imports
from marshmallow import fields

# User model imports
from app import FlaskApp
from api.db.models import (
    IngredientModel,
    MenuItemModel,
    MenuItemCategoryModel,
    OrderItemModel,
    OrderModel,
    UserModel
)

# Initialzie the flask app
app = FlaskApp()


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
