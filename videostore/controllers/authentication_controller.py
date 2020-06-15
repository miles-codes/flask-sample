
from flask import current_app, jsonify, request
from marshmallow import Schema, ValidationError, fields

from ..db import db
from ..lib import generate_jwt, verify_password
from ..models import User


class AuthenticationError(RuntimeError):
    pass


class AuthorizationError(RuntimeError):
    pass


class AuthenticationController:
    @classmethod
    def register_routes(cls, blueprint, prefix_with=None, details=True):
        blueprint.add_url_rule('/login', view_func=login, methods=['POST'])
        blueprint.add_url_rule('/tokens', view_func=tokens, methods=['POST'])


class LoginSchema(Schema):
    username_or_email = fields.String(required=True)
    password = fields.String(required=True)


def login():
    schema = LoginSchema()
    unmarshaled = schema.load(request.json)
    if unmarshaled.errors:
        raise ValidationError(unmarshaled.errors)

    user = User.query.find_by_username_or_email(
        unmarshaled.data['username_or_email']
    ).first()

    if not user:
        raise AuthenticationError("Unknown user")

    if not verify_password(unmarshaled.data['password'], user.password):
        raise AuthenticationError("Invalid password")

    if not user.is_active:
        raise AuthenticationError("Inactive user")

    db.session.add(user)
    db.session.commit()

    response = generate_jwt(
        user=user,
        secret_key=current_app.config['SECRET_KEY'],
        expires_in_seconds=current_app.config['JWT_EXPIRES_IN']
    )
    response['api_key'] = user.api_key

    return jsonify(response)
login.__name__ = 'authentication.login'


def tokens():
    request_api_key = request.json.get('api_key', None)
    if not request_api_key:
        raise AuthenticationError('Missing api_key')

    user = User.query.filter_by(api_key=request_api_key).first()

    if not user:
        raise AuthenticationError('Invalid api_key')

    return jsonify(generate_jwt(
        user=user,
        secret_key=current_app.config['SECRET_KEY'],
        expires_in_seconds=current_app.config['JWT_EXPIRES_IN']
    ))
tokens.__name__ = 'authentication.tokens'
