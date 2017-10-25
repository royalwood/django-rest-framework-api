#pylint:disable=no-member
from io import StringIO
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from universities.models import University
from .models import Subject


STUDENT = 'student@ucroo.com'

class Tests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_superuser(self.uni, STUDENT)
        Subject.objects.create(user=self.user, uni=self.uni, name='foo')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT)
        response = self.client.get(reverse('api:subjects-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'foo')

    def test_upload(self):
        self.login(STUDENT)
        f = StringIO(u'"code", "name"\n"DEV101", "Software Development 101"')
        response = self.client.post(
            reverse('api:subjects-upload'), data={'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
