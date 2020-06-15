from ..models import Category
from ..views import CategorySchema
from .base_controller import ApiController


class CategoryController(ApiController):
    @classmethod
    def endpoint(cls):
        return 'categories'

    @classmethod
    def model(cls):
        return Category

    @classmethod
    def serializer(cls, *args, **kwargs):
        return CategorySchema(*args, **kwargs)
