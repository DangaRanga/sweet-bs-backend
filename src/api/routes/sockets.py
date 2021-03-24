import sys
from typing import Set
from api.db.models import MenuItemCategoryModel
from api.db.schemas import MenuItemCategorySchema
from api.db.models import IngredientModel
from api.db.schemas import IngredientSchema
from api.db.models import UserModel
from api.db.schemas import UserSchema
from api.routes.routes import Routes, app
from signal import *
from eventlet import spawn
import atexit


class ServerSockets():
    """
    This class contains functions to manage the socket 
    based connections in the app
    """

    # A list of possible changes made to a table
    DbActions = ("INSERT", "DELETE", "UPDATE")

    @staticmethod
    def _set_up_change_notifier(conn, table: str, actions: Set[str]):
        """
        Sets up triggers in the Postgres database to notify the app
        when a new menu item is inserted into the databse, a menu item 
        is deleted from the database or a menu item is updated

        Args:
            conn:                   
                A psycopg database connection object. This 
                is used to execute queries

            table (str):            
                The name of the table to watch for changes

            actions (set[str]):     
                The list of Database actions that should trigger a notification.
                Must be one of the strings in DbActions

        Returns:
            str: the name of the channel that pgpubsub should listen on

        Raises:
            TypeError:
                If the actions set has an invalid action. i.e not INSERT, UPDATE or DELETE
        """

        # build function to create in the database
        channel = f"{table}_table_change"
        func_name = f"notify_{table}_change()"
        func = f"""
        CREATE OR REPLACE FUNCTION {func_name}
        RETURNS TRIGGER AS $$
        BEGIN
            PERFORM pg_notify('{channel}','changed');
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """

        # build triggers that will run func on each action
        triggers = ""
        for action in actions:
            if action.upper() in ServerSockets.DbActions:
                trigger_name = f"{table}_notify_{action.lower()}"

                triggers += f"""
                DROP TRIGGER IF EXISTS {trigger_name} ON menuitems;
                CREATE TRIGGER {trigger_name}
                AFTER {action} ON {table}
                FOR EACH ROW EXECUTE PROCEDURE {func_name};
                """
            else:
                raise TypeError(
                    "All actions must be either INSERT, UPDATE or DELETE")

        # insert function and respective triggers into the database
        cur = conn.cursor()
        cur.execute(func)
        if triggers:
            cur.execute(triggers)
        return channel

    @staticmethod
    def get_menuitems_by_category():
        """
        Fetches all menuitems, grouped by category, from the database
        and sends them to all clients connected to the menu namespace

        Args:
            None

        Returns:
            None
        """

        menuitems = MenuItemCategoryModel.query.all()
        category_schema = MenuItemCategorySchema(many=True)
        if menuitems is None:
            app.socketio.emit(
                'error', {"message": "Failed to get menu items", "code": 404}, namespace='/menu/watch')
        else:
            response = category_schema.dump(menuitems)
            app.socketio.emit(
                'changed:menuitems', response, namespace='/menu/watch')

    @staticmethod
    def listen_for_menu():
        """
        Listen for changes to the menuitems table and send an updated
        list of menu items to all clients connected to the menu namespace

        Args:
            None

        Returns:
            NoReturn
        """

        channel = ServerSockets._set_up_change_notifier(
            app.pubsub.conn, "menuitems", set(ServerSockets.DbActions))
        app.pubsub.listen(channel)
        while True:
            for event in app.pubsub.events(yield_timeouts=True):
                if event is None:
                    pass
                else:
                    with app.app_context():
                        ServerSockets.get_menuitems_by_category()

    @staticmethod
    @app.socketio.on('connect', namespace='/menu/watch')
    def on_menu_connect():
        """
        Sends the list of menu items when a client connects to the 
        '/menu/watch' namespace, i.e they connect from the web app's menu.

        Args:
            None

        Returns:
            None
        """

        ServerSockets.get_menuitems_by_category()

    @staticmethod
    def get_users():
        users = UserModel.query.all()
        user_schema = UserSchema(many=True)
        if users is None:
            app.socketio.emit('error', {"message": "Failed to get user list", "code": 404}, namespace='/users/watch')
        else:
            response = user_schema.dump(users)
            app.socketio.emit('changed:users', response, namespace='/users/watch')

    @staticmethod
    def listen_for_users():
        channel = ServerSockets._set_up_change_notifier(app.pubsub.conn, "users", set(ServerSockets.DbActions))
        app.pubsub.listen(channel)
        while True:
            for event in app.pubsub.events(yield_timeouts=True):
                if event is None:
                    pass
                else:
                    with app.app_context():
                        ServerSockets.get_users()

    @staticmethod
    @app.socketio.on('connect', namespace='/users/watch')
    def on_user_connect():
        ServerSockets.get_users()

    @staticmethod
    def get_ingredients():
        ingredients = IngredientModel.query.all()
        ingredient_schema = IngredientSchema(many=True)
        
        if ingredients is None:
            app.socketio.emit(
                'error', {"message": "Failed to get list of ingredients", "code": 404}, namespace='/ingredients/watch'
            )
        else:
            response = ingredient_schema.dump(ingredients)
            app.socketio.emit(
                'changed:ingredients', response, namespace='/ingredients/watch'
            )

    @staticmethod
    def listen_for_ingredients():
        channel = ServerSockets._set_up_change_notifier(
            app.pubsub.conn, "ingredients", set(ServerSockets.DbActions)
        )
        app.pubsub.listen(channel)
        while True:
            for event in app.pubsub.events(yield_timeouts=True):
                if event is None:
                    pass
                else:
                    with app.app_context():
                        ServerSockets.get_ingredients()

    @staticmethod
    @app.socketio.on('connect', namespace='/ingredients/watch')
    def on_shoppinglist_connect():
        ServerSockets.get_ingredients()

    @staticmethod
    @atexit.register
    def clean_up_threads(*args):
        """
        Kills all threads created during app execution. This function is
        intended to run on both normal exit and crashes

        Args:
            *args : The signal and associated frame (not used by this function)

        Returns:
            NoReturn
        """

        for thread in app.socket_threads:
            thread.kill()
        # after killing the threads, remove them from the list
        app.socket_threads.clear()
        sys.exit()

    @staticmethod
    def start_sockets_threads():
        """
        Starts the socket threads and ensures that threads are killed if
        the app crashes.

        Args:
            None

        Returns:
            None

        """

        # register clean_up_threads to run on crash signals
        for sig in (SIGABRT, SIGINT, SIGTERM):
            signal(sig, ServerSockets.clean_up_threads)
        
        # spawn all listen threads
        app.socket_threads.append(spawn(ServerSockets.listen_for_users))
        app.socket_threads.append(spawn(ServerSockets.listen_for_ingredients))
        app.socket_threads.append(spawn(ServerSockets.listen_for_menu))
