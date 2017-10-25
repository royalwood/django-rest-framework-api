from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import Subject


class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'user@ucroo.com')

    def test_string_representation(self):
        subject = Subject(user=self.user, uni=self.uni, name='foo')
        self.assertEqual(str(subject), subject.name)

    def test_add_subject(self):
        Subject.objects.create(user=self.user, uni=self.uni, name='foo')
