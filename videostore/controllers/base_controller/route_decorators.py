from functools import wraps

from flask import request as current_request
from flask import current_app, g

from ...lib import verify_jwt


class SuperUserRequired(RuntimeError):
    def __init__(self):
        super().__init__('Section restricted to admins.')


def jwt_required(view_func):
    """
    View decorator that requires a valid JWT token to be present in the request
    When JWT validation succeeds, it will add User instance related to JWT to
    flask.g (global context variable for current request) as a 'current_user'
    attribute. Then, in a view, you can:

    from flask import g

    if g.current_user.foo:
        ....

    TODO: http://blog.dscpl.com.au/2014/01/implementing-universal-decorator.html
    """

    @wraps(view_func)
    def _wrapper(*args, **kwargs):
        g.current_user = verify_jwt(
            request=current_request,
            secret_key=current_app.config['SECRET_KEY']
        )
        return view_func(*args, **kwargs)

    return _wrapper
