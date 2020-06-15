import datetime
import hashlib
import hmac
import uuid

from passlib.context import CryptContext

import jwt

from .dict_helpers import inverted

PASSLIB_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",

    all__vary_rounds = 0.1,

    # Lower number of rounds because we still want tests to finish in seconds: :)
    pbkdf2_sha256__default_rounds = 1000,
)


class JWTError(RuntimeError):
    pass


def _decode_token(token, secret_key):
    """
    Returns the payload decoded from the given token using the given secret key.
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=secret_key,
            algorithms=['HS512'],
            verify=True,
            options={'require_exp': True},
        )
    except jwt.ExpiredSignature:
        raise JWTError('JWT is expired')
    except jwt.DecodeError:
        raise JWTError("JWT can't be decoded. Invalid signature")

    return payload


def _find_user(jwt_payload):
    """
    Fetches the user DB object using the user id provided in the payload.
    """
    from ..models import User
    user = User.query.filter_by(id=jwt_payload.get('user_id')).first()

    if not user:
        raise JWTError('JWT payload is invalid. Unknown user.')

    return user


def verify_jwt(request, secret_key):
    """
    Verifies the JWT and JWT payload in request using provided secret key.
    """
    from ..models import User

    header = request.headers.get('Authorization', '')

    if not header:
        raise JWTError("Missing 'Authorization' HTTP header")

    parts = header.split()
    if parts[0].lower() != 'bearer':
        raise JWTError('Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError("JWT missing from 'Authorization' HTTP header")
    elif len(parts) > 2:
        raise JWTError("Token contains spaces or is not JWT")

    payload = _decode_token(parts[1], secret_key)

    return _find_user(payload)


def generate_token(user, secret_key, expires_in_seconds, user_roles=[]):
    """
    Generates an access token for the given User using the provided secret key
    and expiration time in seconds.
    """
    from ..models import User

    if not user:
        raise JWTError('Unknown user.')

    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'user_roles': user_roles,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            seconds=expires_in_seconds
        )
    }

    return jwt.encode(payload=payload, key=secret_key, algorithm='HS512')


def generate_jwt(user, secret_key, expires_in_seconds):
    """
    Generates JWT data for given User using provided secret key and expiration
    time in seconds
    """
    return {
        'access_token': generate_token(user, secret_key, expires_in_seconds).decode('utf-8'),
        "token_type": "Bearer",
        "expires_in": expires_in_seconds,
    }


def generate_api_key(user=None):
    # Get a random UUID.
    new_uuid = uuid.uuid4()
    # Hmac that beast.
    return hmac.new(new_uuid.bytes, digestmod=hashlib.sha256).hexdigest()


def password_hash(password):
    return PASSLIB_CONTEXT.encrypt(password)


def verify_password(password, password_hash_value):
    return PASSLIB_CONTEXT.verify(password, password_hash_value)
