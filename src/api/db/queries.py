"""Defines the queries for the schema."""
# Standard imports
import uuid

# User Module imports
from api.db.schema import db, User


class UserQueries():
    def __init___(self):
        """Initialize the class"""
        pass

    # GET queries
    def fetch_all_users(self):
        """Retrieves all user data from the database

        Args:
            None

        Returns:
            A list of dictionaries containing each user's data
        """
        users = User.query.all()
        user_lst = []
        for user in users:
            user_data = self.parse_user_data(user)
            user_lst.append(user_data)
        return user_lst

    def fetch_one_user(self, public_id):
        """Retrieves the data for a user based on their id specified

        Args:
            public_id: The public id of the user being queried for

        Returns:
            user_dict: A dictionary of the user's data
        """
        user = User.query.filter_by(public_id=public_id).first()

        if user is None:
            return {'message': 'User not found'}
        else:
            return self.parse_user_data(user)

    # POST Queries

    def create_user(self, user_data, admin=False):
        """Creates a user in the database

        Args:
            user_data: A json object of the user's data

        Returns:
            None
        """
        new_user = User(public_id=str(uuid.uuid4()),
                        name=user_data['name'],
                        password=user_data['password'],
                        admin=admin)
        db.session.add(new_user)
        db.session.commit()

    def parse_user_data(self, user_obj):
        """Parses user data from the query object

        Args:
            user_obj: The query object for the user

        Returns:
            user_dict: A dictionary with the user's data
        """
        user_dict = {}
        user_dict['public_id'] = user_obj.public_id
        user_dict['name'] = user_obj.name
        user_dict['email'] = user_obj.email
        user_dict['is_admin'] = user_obj.is_admin
        return user_dict
