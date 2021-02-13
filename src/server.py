"""Primary module for running the API."""

import os
from api.routes.routes import app
from api.views.views import Views

if __name__ == '__main__':
    if os.environ.get("IS_DEV"):
        views = Views(app)
    app.db_create_all()
    app.run(host='0.0.0.0', port=9090, debug=True)
