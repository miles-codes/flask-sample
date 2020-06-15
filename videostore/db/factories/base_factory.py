import factory
from faker import Faker
from faker.providers import BaseProvider

from videostore.db import db

# http://fake-factory.readthedocs.io/en/latest/providers.html
fake = Faker()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
