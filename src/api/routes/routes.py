"""Defines the serverside routes for the application."""
# Standard Imports
import os
import sys

# Flask Imports
from flask import request, jsonify
from flask.views import MethodView

# Set up user module imports from root directory of project
from src.api.db.queries import UserQueries


class UserAPI(MethodView):
    """Defines the API methods for a User"""
    endpoint = 'user_api'
    url = '/users'
    p_key = 'user_id'

    def __init__(self):
        """Initializes the class"""
        self.query_obj = UserQueries()

    def get(self, user_id=None):
        """Method for retrieving data

        Args:
            user_id: The id of the desired user

        Returns:
            The a json object of a specific user
        """
        if user_id is None:
            # Fetches all users
            return jsonify({'users': self.query_obj.fetch_all_users()})
        else:
            # Fetch based on user
            return "Some specific user"

    def post(self):
        """Method for adding a user to the database

        Args:
            None

        Returns:
            A status code of 200
        """
        user_data = request.get_json()
        self.query_obj.create_user(user_data)

        return jsonify({'status': 200})

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
