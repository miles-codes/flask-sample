from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class SchoolClass(TimestampedModelMixin, db.Model):
    __tablename__ = 'school_classes'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(
        db.String(255), nullable=False, unique=True, index=True
    )

    #: has_many Student through StudentSchoolClass
    students = db.relationship(
        "Student", secondary="student_school_classes",
        back_populates='school_classes'
    )
