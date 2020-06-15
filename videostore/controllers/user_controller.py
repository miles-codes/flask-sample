
from ..models import User
from ..views import UserSchema
from .base_controller import ApiController


class UserController(ApiController):
    @classmethod
    def endpoint(cls):
        return 'users'

    @classmethod
    def model(cls):
        return User

    @classmethod
    def serializer(cls, *args, **kwargs):
        return UserSchema(*args, **kwargs)
