from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy_repr import PrettyRepresentableBase

from ..db import db


class TimestampedModelMixin(PrettyRepresentableBase):
    """
    Mixed in, this class ensures model has 'created_at' and 'updated_at'
    attributes and also that these are handled correctly when saving the model.
    """

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
         return db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                          onupdate=datetime.utcnow)
