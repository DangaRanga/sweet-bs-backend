# Sweet B's Backend

The API for all proceedings for Sweet B's online store

## Setup

1. Install PostgreSQL [link](https://www.postgresql.org/download/)

2. Create a virtual envirionment
   `python -m venv <your-venv-name>`
3. Install the required packages
   `pip install -r requirements.txt`
4. Perform the Alembic Migrations
   `python src/manage.py db migrate`
   `python src/manage.py db upgrade`
5. Start the server
   `python src/server.py`

And you're good to go!
