from flask.ext.script import Manager
from flask_alembic.cli.script import manager as alembic_manager

from videostore import create_app, environments, lib, models, scripts
from videostore.db import db, factories

if __name__ == '__main__':
    manager = Manager(create_app)

    alembic_manager.add_command('seed', scripts.Seed)
    alembic_manager.add_command('truncate', scripts.Truncate)

    manager.add_command('db', alembic_manager)

    manager.add_command('my_fancy_task', scripts.MyFancyTask)

    manager.add_command('routes', scripts.Routes)

    manager.add_option(
        '-e', '--environment',
        default='development',
        choices=environments.keys(),
        dest='config_environment',
        required=False,
    )

    # Add some more stuff to manager shell so we don't need to import that
    # manually every time
    @manager.shell
    def make_shell_context():
        context = dict(
            app=create_app, db=db,
            models=models,
            factories=factories,
            lib=lib
        )
        context.update(vars(models))
        return context

    manager.run()
