"""University View Tests"""
#pylint:disable=no-member
from io import StringIO

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from .models import University, Campus, School


ADMIN_EMAIL = 'admin@ucroo.com'
STUDENT_EMAIL = 'student@ucroo.com'

class UniversityTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        get_user_model().objects.create_user(self.uni, STUDENT_EMAIL)
        get_user_model().objects.create_superuser(self.uni, ADMIN_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:universities-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)

    def test_patch(self):
        self.login(ADMIN_EMAIL)
        url = reverse('api:universities-detail', args=[self.uni.pk])
        response = self.client.patch(url, {'name': 'Patch university'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch university')


class CampusTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.campus = Campus.objects.create(name='Campus', uni=self.uni)
        get_user_model().objects.create_user(self.uni, STUDENT_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:campuses-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)

    def test_get_unauthenticated_no_uni(self):
        # Must specify the university, otherwise 400
        response = self.client.get(reverse('api:campuses-list'))
        self.assertEqual(response.status_code, 400)

    def test_get_unauthenticated(self):
        response = self.client.get(
            reverse('api:campuses-list'), {'uni': self.uni.pk})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)

    def test_upload(self):
        self.login(STUDENT_EMAIL)
        f = StringIO(u'"name"\n"foo"')
        response = self.client.post(
            reverse('api:campuses-upload'), data={'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SchoolTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.school = School.objects.create(name='School', uni=self.uni)
        get_user_model().objects.create_user(self.uni, STUDENT_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:schools-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)

    def test_get_unauthenticated_no_uni(self):
        # Must specify the university, otherwise 400
        response = self.client.get(reverse('api:schools-list'))
        self.assertEqual(response.status_code, 400)

    def test_get_unauthenticated(self):
        response = self.client.get(
            reverse('api:schools-list'), {'uni':self.uni.pk})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)

    def test_upload(self):
        self.login(STUDENT_EMAIL)
        f = StringIO(u'"name"\n"foo"')
        response = self.client.post(
            reverse('api:schools-upload'), data={'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.course = School.objects.create(name='foo', uni=self.uni)
        get_user_model().objects.create_user(self.uni, STUDENT_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_upload(self):
        self.login(STUDENT_EMAIL)
        f = StringIO(u'"name"\n"foo"')
        response = self.client.post(
            reverse('api:courses-upload'), data={'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
