#pylint:disable=no-member
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from universities.models import University
from .models import Keyword


UNIADMIN = 'uniadmin@ucroo.com'
STUDENT = 'student@ucroo.com'

class Tests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.uniadmin = get_user_model().objects.create_superuser(
            self.uni, UNIADMIN)
        self.keyword = Keyword.objects.create(
            user=self.uniadmin, uni=self.uni, word='foo')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(UNIADMIN)
        response = self.client.get(reverse('api:keywords-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['word'], 'foo')

    def test_post(self):
        self.login(UNIADMIN)
        data = {
            'uni': self.uni.pk,
            'user': self.uniadmin.pk,
            'word': 'foo',
        }
        response = self.client.post(reverse('api:keywords-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        self.login(UNIADMIN)
        url = reverse('api:keywords-detail', args=[self.keyword.pk])
        response = self.client.patch(url, {'word': 'Patch keyword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'patch keyword')

    def test_delete(self):
        self.login(UNIADMIN)
        url = reverse('api:keywords-detail', args=[self.keyword.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
