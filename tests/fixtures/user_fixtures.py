import pytest

from videostore.db.factories import UserFactory
from videostore.models.user import password_hash


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def plaintext_password():
    return "password"
