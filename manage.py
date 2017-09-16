from flask_script import (
    Manager,
    prompt_bool,
    Server,
)

from labeling_api import app
from labeling_api.db import db
from labeling_api.populate_db import populate_db as _populate_db

manager = Manager(app)

manager.add_command('run_api', Server())


@manager.command
def populate_db():
    if app.config.get('TESTING') or app.config.get('DEBUG'):
        db.create_all()
        _populate_db()


@manager.command
def drop_db():
    if prompt_bool('Are you sure?'):
        db.drop_all()


if '__main__' == __name__:
    manager.run()
