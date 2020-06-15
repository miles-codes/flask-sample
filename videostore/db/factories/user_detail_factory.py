from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import UserDetail
from .base_factory import BaseFactory, fake


class UserDetailFactory(BaseFactory):
    class Meta:
        model = UserDetail

    http_account = LazyAttribute(lambda x: fake.url())
    push_url = LazyAttribute(lambda x: fake.url())
    balance = LazyAttribute(lambda x: fake.pyint())
