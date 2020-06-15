from flask import Flask
from flask_alembic import Alembic
from werkzeug.exceptions import default_exceptions

from .controllers import api, build_error_response
from .db import db
from .models import *  # This one is important for Alembic auto generated migrations to work
from .settings import environments


def create_app(config_environment):
    app = Flask('videostore')

    config_object = environments[config_environment]()
    config_object.init_app(app)

    db.init_app(app)

    # Initialize flask-alembic
    alembic = Alembic()
    alembic.init_app(app)

    # Mount blueprints
    app.register_blueprint(api, url_prefix='/api')

    # Log starting of application instance
    app.logger.info(
        "Starting Flask '{0}' in '{1}' mode".format(
            app.name, config_environment
        )
    )

    _initialize_global_exception_handler(app)

    return app


def _initialize_global_exception_handler(app):
    # Following does not work: https://github.com/mitsuhiko/flask/issues/941
    #
    #   @app.errorhandler(HTTPException)
    #   def unhandled_http_error(e):
    #       return build_error_response(e)
    #
    # It was a bug, it was fixed and merged but it will not be in Flask before
    # 1.0 (now is v0.10, there will be no version 0.11)
    #
    # We implement sugested workaround:
    for code, ex in default_exceptions.items():
        app.errorhandler(code)(build_error_response)

    @app.errorhandler(Exception)
    def _unhandled_any_error(e):
        """
        Global, any-unhandled-exception handler.
        Returns API error JSON response.
        """
        return build_error_response(e)
