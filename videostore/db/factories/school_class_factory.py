from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import SchoolClass
from .base_factory import BaseFactory, fake


class SchoolClassFactory(BaseFactory):
    class Meta:
        model = SchoolClass

    name = LazyAttribute(lambda x: fake.name())
