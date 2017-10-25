"""User View Tests"""
#pylint:disable=no-member
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from universities.models import University, Campus, Course
from .models import User


ADMIN_EMAIL = 'admin@ucroo.com'
STUDENT_EMAIL = 'student@ucroo.com'
FRIEND_EMAIL = 'friend@ucroo.com'

class UserTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = User.objects.create_user(self.uni, STUDENT_EMAIL)
        self.admin = User.objects.create_superuser(self.uni, ADMIN_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['uni']['name'], 'foo')

    def test_get_one(self):
        self.login(STUDENT_EMAIL)
        url = reverse('api:users-detail', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.login(ADMIN_EMAIL)
        data = {
            'name': 'New user',
            'email': 'newuser@ucroo.com',
            'uni': self.uni.pk,
            'password': 'foo',
        }
        response = self.client.post(reverse('api:users-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=response.data['id'])
        self.assertTrue(authenticate(username=user.email, password='foo'))

    def test_patch(self):
        self.login(ADMIN_EMAIL)
        url = reverse('api:users-detail', args=[self.admin.pk])
        response = self.client.patch(url, {'name': 'Patch user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch user')


class MakeAdminTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = User.objects.create_user(self.uni, STUDENT_EMAIL)
        Group.objects.create(name='Uni Admin')

    def test(self):
        url = reverse('api:users-makeadmin')
        response = self.client.post(url, {'email': STUDENT_EMAIL})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.groups.filter(name='Uni Admin').exists())

    def test_no_email(self):
        response = self.client.post(reverse('api:users-makeadmin'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Email is required')

    def test_wrong_email(self):
        response = self.client.post(
            reverse('api:users-makeadmin'), {'email': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found')


class RemoveAdminTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = User.objects.create_user(self.uni, STUDENT_EMAIL)
        group = Group.objects.create(name='Uni Admin')
        self.user.groups.add(group)

    def test(self):
        response = self.client.post(
            reverse('api:users-removeadmin'), {'email': STUDENT_EMAIL})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.groups.filter(name='Uni Admin').exists())

    def test_no_email(self):
        response = self.client.post(
            reverse('api:users-removeadmin'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Email is required')

    def test_wrong_email(self):
        response = self.client.post(
            reverse('api:users-removeadmin'), {'email': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found')


class MeTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = User.objects.create_user(self.uni, STUDENT_EMAIL)
        if not self.client.login(username=STUDENT_EMAIL, password='ucroo123'):
            raise ValueError('Could not login')

    def test_get(self):
        response = self.client.get(reverse('api:me-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], STUDENT_EMAIL)

    def test_patch(self):
        response = self.client.patch(
            reverse('api:me-list'), {'name': 'Patch me'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch me')


class ConnectionTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = User.objects.create_user(
            self.uni, STUDENT_EMAIL, name='Student')
        self.friend = User.objects.create_user(
            self.uni, FRIEND_EMAIL, name='Friend')
        self.login(STUDENT_EMAIL)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.student.add_connection(self.friend)
        self.friend.add_connection(self.student)
        response = self.client.get(reverse('api:connections-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Friend')

    def test_connect(self):
        url = reverse('api:users-connect', args=[self.friend.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.student.get_connections()), 1)

    def test_disconnect(self):
        self.student.add_connection(self.friend)
        url = reverse('api:users-disconnect', args=[self.friend.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.student.get_connections()), 0)

    def test_block(self):
        url = reverse('api:users-block', args=[self.friend.pk])
        response = self.client.get(url)
        self.student.add_connection(self.friend)
        self.assertFalse(self.student.is_connected(self.friend))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.student.is_connected(self.friend))
