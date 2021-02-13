from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api.routes.routes import app
import os

app.db_create_all()
migrate = Migrate(app, app.db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()