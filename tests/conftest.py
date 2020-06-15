import os
import sys

import pytest
from unipath import Path

sys.path.append(Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1))

# from fixtures import *
from videostore import create_app
from videostore.db import db as _db
from videostore.db.factories import *
from videostore.models import *


def _delete_all_records(db_obj):
    db_obj.reflect()
    for table_name in reversed([t.name for t in db_obj.metadata.sorted_tables]):
        if table_name != 'alembic_version':
            db_obj.engine.execute(db_obj.table(table_name).delete())
    # _db.drop_all()
    # try:
    #     _db.app.extensions['alembic'].op.drop_table('alembic_version')
    # except Exception:
    #     pass


@pytest.fixture(scope='session')
def app(request):
    """
    Creates session level Flask application object and Flask application
    context. This allows us to work with flask.current_app in tests without
    actually running Flask server
    """
    app = create_app(config_environment='test')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    app.logger.info("Initialized Flask test context")

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def migrated_database(app, request):
    """
    Creates session level fixture that performs Alembic migrations before
    running tests
    """

    _db.app = app
    app.logger.info("Migrating test database...")
    alembic = app.extensions['alembic']
    alembic.upgrade()
    app.logger.info("Migrating test database finished")
    _delete_all_records(_db)

    return _db


@pytest.fixture(scope='function')
def db(migrated_database, request):
    """
    Performs each test methond inside database transaction and rolls back that
    transaction when method finishes
    """
    def _rollback_or_pass():
        # Sometimes session.commit() may fail during tests. This leaves session
        # object unusable for further tests. SQLAlchemy requirest that this object
        # is explicitly rollbacked before it can be used again.
        # In other cases, we try to rollback the session transaction that was
        # already commited. This will rise exception which we don't care about:
        # session object is still usable after the fact.
        try:
            migrated_database.session.rollback()
        except Exception:
            pass

    def teardown():
        _rollback_or_pass()
        _delete_all_records(migrated_database)

    request.addfinalizer(teardown)

    return migrated_database
