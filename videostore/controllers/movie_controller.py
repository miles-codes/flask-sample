from ..models import Movie
from ..views import MovieSchema
from .base_controller import ApiController


class MovieController(ApiController):
    @classmethod
    def endpoint(cls):
        return 'movies'

    @classmethod
    def model(cls):
        return Movie

    @classmethod
    def serializer(cls, *args, **kwargs):
        return MovieSchema(*args, **kwargs)
