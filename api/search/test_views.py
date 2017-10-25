#pylint:disable=no-member
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from universities.models import University
from core.models import Category
from marketplace.models import Item
from subjects.models import Subject
from groups.models import (
    Club, CustomGroup, StudentService, StudyGroup, MentorGroup)


STUDENT = 'student@ucroo.com'

class Tests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_superuser(
            self.uni, STUDENT, name='Student')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_no_query(self):
        self.login(STUDENT)
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'student'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'Student')

    def test_get_item(self):
        category = Category.objects.create(name='bar', module='marketplace')
        Item.objects.create(
            user=self.user, title='foo', category=category, price=10.00)
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_subject(self):
        Subject.objects.create(user=self.user, uni=self.uni, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_club(self):
        Club.objects.create(user=self.user, uni=self.uni, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_customgroup(self):
        CustomGroup.objects.create(user=self.user, uni=self.uni, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_studentservice(self):
        StudentService.objects.create(user=self.user, uni=self.uni, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_studygroup(self):
        StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')

    def test_get_mentorgroup(self):
        MentorGroup.objects.create(user=self.user, uni=self.uni, name='foo')
        self.login(STUDENT)
        response = self.client.get(reverse('search'), {'q': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'foo')
