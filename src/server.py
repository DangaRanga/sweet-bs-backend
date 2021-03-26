"""Primary module for running the API."""

import os
from api.routes.sockets import ServerSockets, app
from api.views.views import Views
from eventlet import monkey_patch

from app import FlaskApp


if __name__ == '__main__':
    monkey_patch()
    if os.environ.get("IS_DEV"):
        views = Views(app)
    app.db_create_all()
    ServerSockets.start_sockets_threads()
    app.socketio.run(app, "0.0.0.0", 9090, debug=True)
