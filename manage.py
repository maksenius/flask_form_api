from app import db, create_app
from config import CURRENT_CONFIG
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(CURRENT_CONFIG)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
