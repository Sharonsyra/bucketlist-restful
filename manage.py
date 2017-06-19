import os
import unittest

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app.bucketlist.views import db, create_app

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """manager command to run unittests."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def createdb():
    """ Creates database and its tables """
    db.create_all()
    db.session.commit()


@manager.command
def dropdb():
    """ Deletes database """
    if prompt_bool("Are you sure you want to delete?"):
        db.drop_all()


if __name__ == '__main__':
    manager.run()
