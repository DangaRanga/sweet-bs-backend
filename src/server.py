"""Primary module for running the API."""

# Flask imports
from flask import Flask
import os

# User module imports
from api.routes.routes import UserAPI, OrdersAPI, IngredientsAPI
from api.db.schema import db
from config.config import Config, app_config


class FlaskApp(Flask):

    def __init__(self, import_name):
        # Inherit class methods from Flask
        super(FlaskApp, self).__init__(import_name)

        # Configure the Flask app
        self.config.from_object(Config)

        # Register the endpoints for the routes
        self.register_apis()
        self.config.from_object(app_config)

        # Initialize the SQLAlchemy Database
        db.init_app(self)
        with self.app_context():
            db.create_all()

    def register_api(self, view, endpoint, url, p_key='id', p_key_type='int'):
        """Generalized method for registering new views/API endpoints

        Args:
            view: The MethodView object
            endpoint: The endpoint for the api
            url: The url string for the api
            p_key: The field for the primary key of the database entry for the
                    api

        Returns:
            None
        """
        view_function = view.as_view(endpoint)

        # Setting up URL rule for GET Method without priamry key
        self.add_url_rule(url, view_func=view_function, methods=['GET'])

        # Setting up URL rule for POST Method
        self.add_url_rule(url, view_func=view_function, methods=['POST'])

        # Setting up URL Rule for GET, POST and DELETE
        self.add_url_rule(f'{url} {p_key_type} {p_key}',
                          view_func=view_function,
                          methods=['GET', 'DELETE', 'PUT'])

    def register_apis(self):
        view_lst = [UserAPI, OrdersAPI, IngredientsAPI]
        for view in view_lst:
            self.register_api(view, view.endpoint, view.url, view.p_key)



app = FlaskApp(__name__)
db.init_app(app)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080)
