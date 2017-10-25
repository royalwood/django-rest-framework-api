"""Marketplace View Tests"""
#pylint:disable=no-member
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from universities.models import University
from core.models import Category
from .models import Item


ADMIN_EMAIL = 'admin@ucroo.com'
STUDENT_EMAIL = 'student@ucroo.com'
FRIEND_EMAIL = 'friend@ucroo.com'

class Tests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, STUDENT_EMAIL)
        self.category = Category.objects.create(
            name='Test', module='marketplace')
        self.item = Item.objects.create(
            user=self.user, title='foo', category=self.category, price=10.00)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:marketplaceitems-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.login(STUDENT_EMAIL)
        data = {
            'user': self.user.pk,
            'title': 'foo',
            'category': self.category.pk,
            'price': '10.00',
        }
        response = self.client.post(reverse('api:marketplaceitems-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.all().count(), 2)
