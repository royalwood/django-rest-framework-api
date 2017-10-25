from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import Subject
from .resources import SubjectResource


STUDENT_EMAIL = 'student@ucroo.com'

class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, STUDENT_EMAIL)

    def test_add(self):
        resource = SubjectResource()
        csv = '"code","name"\n"foo","bar"'
        result = resource.import_csv(csv, self.uni, self.user)
        self.assertFalse(result.has_errors())
        subject = Subject.objects.all().last()
        self.assertEqual(subject.code, 'foo')
        self.assertEqual(subject.name, 'bar')

    def test_update(self):
        Subject.objects.create(user=self.user, uni=self.uni, code='foo')
        resource = SubjectResource()
        csv = '"code","name"\n"foo","bar"'
        result = resource.import_csv(csv, self.uni, self.user)
        self.assertFalse(result.has_errors())
        subjects = Subject.objects.all()
        self.assertEqual(len(subjects), 1)
