import logging

import requests
from flask import request as flask_request
from flask import g, jsonify
from flask.views import MethodView

from ...db import db
from .pagination import ResponsePaginator
from .route_decorators import jwt_required

logger = logging.getLogger('videostore')


class NotImplementedZomgError(NotImplementedError):
    def __init__(self):
        super().__init__(
            'Somebody forgot to implement this. ' +
            'Try asking developers, some of them are certainly capable of ' +
            'doing this kind of stuff ' +
            '- but remember to bring beer and pizza with you'
        )


class BaseController(MethodView):
    AUTHENTICATION_DECORATORS = [jwt_required]
    HEADERS_DECORATORS = []
    PERMISSION_DECORATORS = []

    @classmethod
    def register_routes(cls, blueprint, prefix_with=None, details=True, id_param_name='id'):
        """
        From: http://flask.pocoo.org/docs/0.10/views/
        Registers MethodView subclass routes
        """
        url_prefix = '/{0}'.format(prefix_with) if prefix_with else ""
        url = url_prefix + '/{0}'.format(cls.endpoint())
        details_url = url + '/<' + (id_param_name or 'id') + '>'

        if 'GET' in cls.methods:
            blueprint.add_url_rule(url, view_func=cls.as_view(cls.endpoint() + '.list'), methods=['GET', ])
            if details:
                blueprint.add_url_rule(details_url, view_func=cls.as_view(cls.endpoint() + '.show'), methods=['GET', ])

        if 'POST' in cls.methods:
            blueprint.add_url_rule(url, view_func=cls.as_view(cls.endpoint() + '.create'), methods=['POST', ])

        if 'PUT' in cls.methods and details:
            blueprint.add_url_rule(details_url, view_func=cls.as_view(cls.endpoint() + '.update'), methods=['PUT', ])

        if 'DELETE' in cls.methods and details:
            blueprint.add_url_rule(details_url, view_func=cls.as_view(cls.endpoint() + '.destroy'), methods=['DELETE', ])

    @classmethod
    def _decorate(cls, view_func, name):
        """
        Decorates view_func with all needed decorators.
        This is to allow to plug in for example jwt_required and permission
        decorators for each of view callables
        """

        # Order is important: auth decorators should always come last
        decorators = (
            cls.PERMISSION_DECORATORS +
            cls.HEADERS_DECORATORS +
            cls.AUTHENTICATION_DECORATORS
        )

        for decorator in decorators:
            view_func = decorator(view_func)

        # We attach the view class to the view function for two reasons:
        # first of all it allows us to easily figure out what class-based
        # view this thing came from, secondly it's also used for instantiating
        # the view class so you can actually replace it with something else
        # for testing purposes and debugging.
        view_func.__name__ = name
        view_func.view_class = cls
        view_func.__doc__ = cls.__doc__
        view_func.__module__ = cls.__module__

        return view_func

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        """
        We override base class method because we need finer grained controll
        over what gets decorated with what.

        Converts the class into an actual view function that can be used
        with the routing system.  Internally this generates a function on the
        fly which will instantiate the :class:`View` on each request and call
        the :meth:`dispatch_request` method on it.

        The arguments passed to :meth:`as_view` are forwarded to the
        constructor of the class.
        """
        def view(*args, **kwargs):
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)

        view = cls._decorate(view, name)

        return view

    @property
    def request(self):
        return flask_request

    @property
    def current_user(self):
        return g.current_user

    def get(self, id=None):
        if id:
            schema = self.serializer()
            return jsonify(schema.dump(self.get_one(id)).data)

        schema = self.serializer(many=True)

        paginator = ResponsePaginator(self.get_list())
        response = paginator.page_dict()
        response['objects'] = schema.dump(response['objects']).data
        return jsonify(response)

    def post(self):
        logger.debug('Request: %s', self.request)
        logger.debug('Payload: %s', self.request.get_json(silent=True))
        logger.debug('Headers: %s', self.request.headers)

        obj = self.create()
        schema = self.serializer()
        response = jsonify(schema.dump(obj).data)
        response.status_code = requests.codes.CREATED
        return response

    def put(self, id):
        logger.debug('Request: %s', self.request)
        logger.debug('Payload: %s', self.request.get_json(silent=True))
        logger.debug('Headers: %s', self.request.headers)

        obj = self.update(id)
        schema = self.serializer()
        response = jsonify(schema.dump(obj).data)
        response.status_code = requests.codes.OK
        return response

    def delete(self, id):
        obj = self.get_one(id)
        db.session.delete(obj)
        db.session.commit()
        response = jsonify({})
        response.status_code = requests.codes.OK
        return response
