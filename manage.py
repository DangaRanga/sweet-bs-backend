from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.server import app, db
import os


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    print("\napp",app.config)
    manager.run()