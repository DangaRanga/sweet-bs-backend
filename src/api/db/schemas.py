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

    class CategorySchema(app.ma.SQLAlchemyAutoSchema):
        class Meta:
            model = MenuItemCategoryModel

    ingredients = app.ma.Nested(IngredientSchema, default=[], many=True)
    category = app.ma.Nested(CategorySchema)


class OrderItemSchema(app.ma.SQLAlchemyAutoSchema):

    class Meta:
        model = OrderItemModel
        include_fk = True
        #exclude = ("menuitem_id", "order_id")

    menuitem = app.ma.Nested(MenuItemSchema, default={'price': 0})


class UserSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ("_password",)

    password = fields.String(attribute='_password')
    orders_placed = fields.Integer(attribute='orders_placed')


class OrderSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        exclude = ("user_id",)

    items = app.ma.Nested(OrderItemSchema, default=[], many=True)
    user = app.ma.Nested(UserSchema, default={
        'address': '',
        'firstname': '',
        'lastname': ''
    })


class MenuItemCategorySchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemCategoryModel

    menuitems = app.ma.Nested(MenuItemSchema, many=True, default=[])
