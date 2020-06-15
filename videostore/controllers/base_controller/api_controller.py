import logging

from flask import abort, g
from marshmallow import ValidationError

from ...db import db
from .base_controller import BaseController, NotImplementedZomgError

logger = logging.getLogger('videostore')


class ApiController(BaseController):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    @classmethod
    def endpoint(cls):
        """Flask endpoint root."""
        raise NotImplementedZomgError

    @classmethod
    def model(cls):
        """Model class used by this controller."""
        raise NotImplementedZomgError

    @classmethod
    def serializer(cls, *args, **kwargs):
        """ Instance of serializer class used by this controller."""
        raise NotImplementedZomgError

    @classmethod
    def query(self):
        """Default query for controller."""
        return self.model().query

    def get_list(self):
        """GET /endpoint, ie. /categories"""
        return self.query()

    def get_one(self, id):
        """GET /endpoint/id, ie. /categories/42"""
        found = self.query().filter_by(id=id).first()
        if not found:
            abort(404)
        return found

    def validate(self):
        json_data = self.request.json or {}
        schema = self.serializer(exclude='id')
        params = schema.load(json_data)

        if params.errors:
            raise ValidationError(params.errors)

        return params.data

    def create(self):
        """POST /endpoint, ie. /categories"""
        params = self.validate(schema)

        if 'id' in params:
            del(params['id'])

        obj = self.model()(**params)
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, id):
        """PUT /endpoint/<id>, ie. /categories/42"""
        params = self.validate()
        obj = self.get_one(id)
        for k, v in params.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()
        return obj
