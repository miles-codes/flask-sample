from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import Movie
from .base_factory import BaseFactory, fake


class MovieFactory(BaseFactory):
    class Meta:
        model = Movie

    title = LazyAttribute(lambda x: fake.catch_phrase())

    #: belongs_to Category
    category = SubFactory('videostore.db.factories.CategoryFactory')
