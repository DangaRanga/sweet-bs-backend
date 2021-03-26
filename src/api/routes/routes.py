# Flask imports
from functools import wraps
from flask import jsonify, request, make_response, abort
from werkzeug.exceptions import HTTPException


# Database importsfrom marshmallow.fields import Integer
from api.db.models import (
    IngredientModel,
    MenuItemCategoryModel,
    MenuItemModel,
    OrderItemModel,
    OrderModel,
    UserModel,
    app)

from api.db.schemas import (
    IngredientSchema,
    MenuItemCategorySchema,
    MenuItemSchema,
    OrderSchema,
    UserSchema,
)


# JWT Authentication Imports
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from datetime import datetime, timedelta
from method_decorator import method_decorator


class Routes():
    @staticmethod
    @app.after_request
    def add_response_headers(response=None):
        if not response:
            response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        return response

    class token_required(method_decorator):
        """Decorator to verify the JWT.

        Inherits the method_decorator as a wrapper class to provide the
        __name__ attribute
        """

        def __call__(self, *args, **kwargs):
            token = None

            # Retrieve the JWT from the request header
            if 'X-Access-Token' in request.headers:
                token = request.headers['X-Access-Token']

            # Returns a 401 if there is no token
            if not token:
                abort(make_response({"message": 'The Token is missing'}, 401))

            # Decode the token to retrieve the user requesting the data
            try:
                data = jwt.decode(token, app.config.get(
                    'SECRET_KEY'), algorithms="HS256")
                current_user = UserModel.query.filter_by(
                    public_id=data.get('public_id')).first()

            except InvalidSignatureError:
                abort(make_response({"message": 'Token is invalid'}, 401))

            except ExpiredSignatureError:
                abort(make_response({"message": 'Token is expired'}, 401))

            return method_decorator.__call__(
                self, current_user, *args, **kwargs)

    # Authentication routes

    @staticmethod
    @app.route("/auth/login", methods=['POST'])
    def login():
        """Route for handling user login

        Args:
            None

        Returns:
            A JSON response with the JWT if the user is succesfully logged in
            and a 202 response code.

            If the user data is invalid or not found, a 401 response is
            returned
        """

        # Retrieve login details from request
        req = request.get_json(force=True)
        username = req.get('username')
        password = req.get('password')

        # Check if the fields were successfully recieved, if not return a 401
        if username is None or password is None:
            return make_response(
                'Could not verify user',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login details required"'})

        user = UserModel.query.filter_by(username=username).first()

        # Return a 401 if no user is found
        if user is None:
            return abort(make_response(
                {"message": 'Could not verify user'},
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist"'}))

        # Verify user password
        if user.check_password(password) is True:
            expiry_time = app.config.get('JWT_ACCESS_LIFESPAN').get('hours')

            # Generate the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(hours=expiry_time),
                'admin': user.is_admin
            }, app.config.get('SECRET_KEY'), algorithm="HS256")

            return make_response(jsonify(
                {'token': token}), 202)
        else:
            return make_response(
                {"message": 'Invalid password'},
                401,
                {'WWW-Authenticate': 'Basic realm="Wrong password"'}
            )

    @staticmethod
    @app.route("/auth/signup", methods=['POST'])
    def signup():
        """Route to retrieve details to signup a user up

        Args:
            None

        Returns:
            response_code: 201 if the registration is succesful
                           401 if the user already exists
        """

        # Retrieve signup details from form
        req = request.get_json(force=True)

        # TODO - Validate user data @Deniz
        username = req.get('username')

        # Check if the user already exists
        user = UserModel.query.filter_by(username=username).first()

        # Create and insert new user
        if user is None:
            user = UserModel(
                username=username,
                first_name=req.get('firstname'),
                last_name=req.get('lastname'),
                password=req.get('password'),
                email=req.get('email'),
                address=req.get('address')
            )

            app.db.session.add(user)
            app.db.session.commit()
            return make_response('Successfully registered.', 201)
        return make_response('User already exists. Please Log in', 401)

    @ staticmethod
    @ app.route("/users", methods=['GET'])
    def get_all_users():
        """Queries the User table for all users

        Args:
            current_user: The user currently authenticated

        Returns:
            A json object containing all users
        """
        # print(current_user.username)
        users = UserModel.query.all()
        user_schema = UserSchema(many=True)
        if users is None:
            response = {
                "message": "no users found",
            }
            return jsonify(response)
        else:
            response = user_schema.dump(users)
            return (jsonify(response))

    @staticmethod
    @app.route("/users/remove", methods=['POST'])
    def remove_user():
        req = request.get_json(force=True)
        try:
            uid = int(req.get('id'))
            user = UserModel.query.get(uid)
            app.db.session.delete(user)
            app.db.session.commit()
            res = 'User %s successfully deleted.' % (user.firstname)
        except:
            res = 'User could not be deleted'
        return (jsonify({'res': res}))

    @ staticmethod
    @ app.route("/orders", methods=['GET'])
    def get_all_orders():
        """Queries the Orders table for all orders.

        Args:
            current_user: The user currently authenticated

        Returns:
            A json object containing all orders
        """

        orders = OrderModel.query.all()
        order_schema = OrderSchema(many=True)
        if orders is None:
            response = {
                "message": "no orders found",
            }
            return jsonify(response)
        else:
            response = order_schema.dump(orders)
            return jsonify(response)

    @staticmethod
    @app.route("/orders/add", methods=['POST'])
    @token_required
    def add_new_order(customer: UserModel):
        """
        Adds a new order to the database

        Args:
            customer (UserModel): the customer who made the order

        Returns:
            Response
        """

        orderjson = request.json
        complete = orderjson["complete"]
        user = customer.id
        items = orderjson["items"]
        # create order
        order = OrderModel(complete=complete, user_id=user)
        app.db.session.add(order)
        app.db.session.flush()
        # get the id of the order
        newid = order.id
        # register all the items on the order
        for item in items:
            oitem = OrderItemModel(
                menuitem_id=item["menuitem"]["id"],
                order_id=newid,
                qty=item["qty"]
            )
            app.db.session.add(oitem)
        # complete add order
        app.db.session.commit()
        return make_response("Order added succesfully", 201)

    @ staticmethod
    @ app.route("/menuitems", methods=['GET'])
    def get_all_menuitems():
        """Queries the MenuItem table for all menuitems

        Args:
            None

        Returns:
            A json object containing all menuitems
        """

        menuitems = MenuItemModel.query.join(
            MenuItemCategoryModel,
            MenuItemModel.category_id == MenuItemCategoryModel.id)

        menuitem_schema = MenuItemSchema(many=True)
        if menuitems is None:
            response = {
                "message": "no menuitems found",
            }
            return jsonify(response)
        else:
            response = menuitem_schema.dump(menuitems)
            return jsonify(response)

    @ staticmethod
    @ app.route("/ingredients", methods=['GET'])
    def get_all_ingredients():
        """Queries the Ingredients table for all ingredients

        Args:
            current_user: The user currently authenticated

        Returns:
            A json object containing all ingredients
        """

        ingredients = IngredientModel.query.all()
        ingredient_schema = IngredientSchema(many=True)
        if ingredients is None:
            response = {
                "message": "no ingredients found",
            }
            return jsonify(response)
        else:
            response = ingredient_schema.dump(ingredients)
            return jsonify(response)

    @staticmethod
    @app.route('/ingredients/setstock', methods=['POST'])
    def set_stock():
        req = request.get_json(force=True)
        try:
            stock = req.get('stock')
            uid = int(req.get('id'))
            if stock == 'yes':
                app.db.session.execute(
                    'UPDATE ingredients SET in_stock = true WHERE id = :val', {'val': uid})
                app.db.session.commit()
                res = 'Stock updated.'
            elif stock == 'no':
                app.db.session.execute(
                    'UPDATE ingredients SET in_stock = false WHERE id = :val', {'val': uid})
                app.db.session.commit()
                res = 'Stock updated.'
            else:
                res = 'A problem occured'
        except:
            res = 'Database could not be updated'

        return (jsonify({'res': res}))

    @staticmethod
    @app.errorhandler(HTTPException)
    def http_errors_to_json(error: HTTPException):
        """
        General error handler to ensure that the server always returns JSON
        """

        response = {
            "message": str(error.description),
        }
        response = jsonify(response)
        response.status_code = error.code
        return response
