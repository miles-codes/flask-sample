from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import Category
from .base_factory import BaseFactory, fake


class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    name = LazyAttribute(lambda x: fake.color_name())
