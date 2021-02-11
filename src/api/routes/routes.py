"""Defines the serverside routes for the application."""
from flask.views import MethodView


class UserAPI(MethodView):
    """Defines the API methods for a User"""
    endpoint = 'user_api'
    url = '/users'
    p_key = 'user_id'

    def __init__(self):
        """Initializes the class"""
        pass

    def get(self, user_id=None):
        """Method for retrieving data

        Args:
            user_id: The id of the desired user

        Returns:
            The data for the specified user, or all users from the database
        """
        if user_id is None:
            # Fetches all users
            return "Testing User API"
        else:
            # Fetch based on user
            return "Hey im a user"

    def post(self):
        """Method for adding data to the database

        Args:
            None

        Returns:
            status_code
        """
        pass

    def delete(self, id):
        """Method for deleting an item based on its id

        Args:
            id

        Returns:
            status_code
        """
        pass

    def put(self, id):
        """Method for updating user data

        Args:
            id
        """
        pass


class OrdersAPI(MethodView):
    endpoint = 'order_api'
    url = '/orders'
    p_key = 'order_id'

    def __init__(self):
        """Initializes the class"""
        pass


class IngredientsAPI(MethodView):
    endpoint = 'ingredients_api'
    url = '/ingredients'
    p_key = 'ingredient_id'

    def __init__(self):
        """Initializes the class"""
        pass


class MenuItemAPI(MethodView):
    endpoint = 'menuitem_api'
    url = '/menuitems'
    p_key = 'menu_item_id'

    def __init__(self):
        """Initializes the class"""
        pass
