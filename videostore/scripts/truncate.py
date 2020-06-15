from flask import current_app
from flask_script import Command, prompt_bool

from ..db import db


class Truncate(Command):

    """ Truncates all tables in current database """

    def run(self):
        if prompt_bool(
            "You are trying to delete all records in database! Type 'yes' if you are sure",
            default=False,
            yes_choices=('yes')
        ):
            current_app.logger.info('Truncating...')
            db.reflect()
            for table_name in reversed([t.name for t in db.metadata.sorted_tables]):
                if table_name != 'alembic_version':
                    db.engine.execute(db.table(table_name).delete())
        else:
            current_app.logger.info('Not doing anything...')
