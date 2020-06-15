from ..db import db
from .timestamped_mixin import TimestampedModelMixin


class StudentSchoolClass(TimestampedModelMixin, db.Model):
    __tablename__ = 'student_school_classes'

    id = db.Column(db.BigInteger, primary_key=True)

    student_id = db.Column(
        db.BigInteger,
        db.ForeignKey('students.id'), nullable=False, index=True
    )
    student = db.relationship("Student", uselist=False)

    school_class_id = db.Column(
        db.BigInteger,
        db.ForeignKey('school_classes.id'), nullable=False, index=True
    )
    school_class = db.relationship("SchoolClass", uselist=False)
