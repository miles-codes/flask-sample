from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class Student(TimestampedModelMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(
        db.String(255), nullable=False, unique=True, index=True
    )

    # belongs_to_many SchoolClass through StudentSchoolClass
    school_classes = db.relationship(
        "SchoolClass", secondary="student_school_classes",
        back_populates="students"
    )
