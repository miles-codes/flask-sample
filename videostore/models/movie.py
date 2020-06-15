from datetime import datetime

from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class Movie(TimestampedModelMixin, db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(
        db.String(255), nullable=False, unique=True, index=True
    )

    #: belongs_to Category
    category_id = db.Column(
        db.BigInteger,
        db.ForeignKey('categories.id', ondelete='RESTRICT'),
        nullable=False, index=True
    )
    category = db.relationship(
        'Category', back_populates='movies', uselist=False
    )
