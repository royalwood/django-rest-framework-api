from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from core.models import Category
from marketplace.models import Item
from subjects.models import Subject
from groups.models import (
    Club, CustomGroup, StudentService, StudyGroup, MentorGroup)
from .serializers import SearchSerializer


class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'foo@bar.com', name='foo')

    def test_user(self):
        context = {'auth_user': self.user}
        serializer = SearchSerializer(self.user, context=context)
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['email'], 'foo@bar.com')

    def test_item(self):
        category = Category(name='Test', module='marketplace')
        item = Item(user=self.user, title='foo', category=category, price=10.00)
        serializer = SearchSerializer(item, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['price'], '10.00')

    def test_subject(self):
        subject = Subject(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(subject, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_club(self):
        group = Club(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_customgroup(self):
        group = CustomGroup(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_studentservice(self):
        group = StudentService(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_studygroup(self):
        group = StudyGroup(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_mentorgroup(self):
        group = MentorGroup(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')

    def test_customgroup(self):
        group = CustomGroup(user=self.user, uni=self.uni, name='foo')
        serializer = SearchSerializer(group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['label'], 'foo')
        self.assertEqual(serializer.data['data']['name'], 'foo')
