from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import Student
from .base_factory import BaseFactory, fake


class StudentFactory(BaseFactory):
    class Meta:
        model = Student

    name = LazyAttribute(lambda x: fake.name())
