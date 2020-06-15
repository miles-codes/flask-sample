from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import Role
from .base_factory import BaseFactory, fake


class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    name = LazyAttribute(lambda x: fake.job())
