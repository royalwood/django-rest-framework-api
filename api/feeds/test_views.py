"""Feeds View Tests"""
#pylint:disable=no-member
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from universities.models import University
from .models import Post, PostLog


ADMIN_EMAIL = 'admin@ucroo.com'
STUDENT_EMAIL = 'student@ucroo.com'
FRIEND_EMAIL = 'friend@ucroo.com'

class PostTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, STUDENT_EMAIL)
        self.post = Post.objects.create(
            user=self.student, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(STUDENT_EMAIL)
        response = self.client.get(reverse('api:posts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one(self):
        self.login(STUDENT_EMAIL)
        url = reverse('api:posts-detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], 'foo')


class CommentTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, STUDENT_EMAIL)
        self.post = Post.objects.create(
            user=self.student, uni=self.uni, feed_object='university',
            feed_object_id=1, body='test')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        """Any authenticated user can get groups"""
        self.login(STUDENT_EMAIL)
        response = self.client.get(
            reverse('api:postcomments-list'), {'post': self.post.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
