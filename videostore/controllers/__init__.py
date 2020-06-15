from flask import Blueprint

from .authentication_controller import AuthenticationController
from .base_controller import ApiController, build_error_response
from .category_controller import CategoryController
from .movie_controller import MovieController
from .user_controller import UserController

"""
Blueprint for /api routes
"""
api = Blueprint('api', 'videostore')


@api.record
def routes(setup_state):
    from ..lib import leaf_subclasses

    api.config = setup_state.app.config
    api.logger = setup_state.app.logger

    for klass in (
        leaf_subclasses(ApiController) + [AuthenticationController]
    ):
        klass.register_routes(api)
