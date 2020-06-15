from datetime import datetime

from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class Category(TimestampedModelMixin, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(
        db.String(255), nullable=False, unique=True, index=True
    )

    #: has_many Movie
    movies = db.relationship('Movie', back_populates='category')
