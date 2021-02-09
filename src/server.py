"""Primary module for running the API."""

from config.config import FlaskApp

if __name__ == '__main__':
    app = FlaskApp(__name__)
    app.run(host='0.0.0.0', port=8080)
