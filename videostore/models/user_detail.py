from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class UserDetail(TimestampedModelMixin, db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.BigInteger, primary_key=True)

    http_account = db.Column(
        db.String(1024), nullable=True, unique=False, index=False
    )
    push_url = db.Column(
        db.String(2048), nullable=True, unique=False, index=False
    )
    balance = db.Column(
        db.BigInteger, nullable=False, default=0, server_default="0"
    )

    #: belongs_to User
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False, index=True
    )
    user = db.relationship('User', back_populates='user_details', uselist=False)
