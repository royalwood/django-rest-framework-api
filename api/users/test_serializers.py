from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .serializers import UserSerializer, FullUserSerializer


class UserSerializerTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'test@ucroo.com')

    def test(self):
        UserSerializer(self.user, context={'auth_user': self.user})


class FullUserSerializerTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'test@ucroo.com')

    def test(self):
        serializer = FullUserSerializer(self.user)
        self.assertEqual(serializer.data['total_accepted_connections'], 0)
