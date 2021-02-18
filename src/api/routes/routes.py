from flask.globals import request
from flask.helpers import make_response
from marshmallow.fields import Integer
from api.db.models import IngredientModel, IngredientSchema, MenuItemCategoryModel, MenuItemCategorySchema, MenuItemModel, MenuItemSchema, OrderModel, OrderSchema, UserSchema, UserModel, app
from flask import jsonify

class Routes():
    @staticmethod
    def _response_headers(response=None):
        if not response:
            response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        return response

    @staticmethod
    @app.route("/users", methods=['GET', 'OPTIONS'])
    def get_all_users():
        if request.method=="OPTIONS":
            return Routes._response_headers()
        users = UserModel.query.all()
        user_schema = UserSchema(many=True)
        if users is None:
            response = {
                "message":"no users found",
            }
            return jsonify(response)
        else:
            response = user_schema.dump(users)
            return Routes._response_headers(jsonify(response))

    @staticmethod
    @app.route("/orders", methods=['GET','OPTIONS'])
    def get_all_orders():
        if request.method=="OPTIONS":
            return Routes._response_headers()
        orders = OrderModel.query.all()
        order_schema = OrderSchema(many=True)
        if orders is None:
            response = {
                "message":"no orders found",
            }
            return Routes._response_headers(jsonify(response))
        else:
            response = order_schema.dump(orders)
            return Routes._response_headers(jsonify(response))

    @staticmethod
    @app.route("/menuitems", methods=['GET','OPTIONS'])
    def get_all_menuitems():
        if request.method=="OPTIONS":
            return Routes._response_headers()
        menuitems = MenuItemModel.query.join(MenuItemCategoryModel,MenuItemModel.category_id==MenuItemCategoryModel.id)
        menuitem_schema = MenuItemSchema(many=True)
        if menuitems is None:
            response = {
                "message":"no menuitems found",
            }
            return Routes._response_headers(jsonify(response))
        else:
            response = menuitem_schema.dump(menuitems)
            return Routes._response_headers(jsonify(response))

    @staticmethod
    @app.route("/ingredients", methods=['GET','OPTIONS'])
    def get_all_ingredients():
        if request.method=="OPTIONS":
            return Routes._response_headers()
        ingredients = IngredientModel.query.all()
        ingredient_schema = IngredientSchema(many=True)
        if ingredients is None:
            response = {
                "message":"no ingredients found",
            }
            return Routes._response_headers(jsonify(response))
        else:
            response = ingredient_schema.dump(ingredients)
            return Routes._response_headers(jsonify(response))

    @staticmethod
    @app.route("/menuitems/category", methods=['GET','OPTIONS'])
    def get_menuitems_by_category():
        if request.method=="OPTIONS":
            return Routes._response_headers()
        menuitems = MenuItemCategoryModel.query.all()
        category_schema = MenuItemCategorySchema(many=True)
        if menuitems is None:
            response = {
                "message":"no menuitems found",
            }
            return Routes._response_headers(jsonify(response))
        else:
            response = category_schema.dump(menuitems)
            return Routes._response_headers(jsonify(response))