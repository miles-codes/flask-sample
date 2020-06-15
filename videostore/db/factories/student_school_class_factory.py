from factory import LazyAttribute, RelatedFactory, Sequence, SubFactory

from ...models import StudentSchoolClass
from .base_factory import BaseFactory, fake


class SchoolClassFactory(BaseFactory):
    class Meta:
        model = StudentSchoolClass

    student = SubFactory('videostore.db.factories.StudentFactory')
    school_class = SubFactory('videostore.db.factories.SchoolClassFactory')
