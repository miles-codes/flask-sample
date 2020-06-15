from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import Country
from .base_factory import BaseFactory, fake


class CountryFactory(BaseFactory):
    class Meta:
        model = Country

    name = LazyAttribute(lambda x: fake.country())
