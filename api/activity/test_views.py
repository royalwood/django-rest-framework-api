#pylint:disable=no-member
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from universities.models import University
from groups.models import Club, ClubMember
from actstream.models import Follow


STUDENT = 'student@ucroo.com'

class Tests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, STUDENT, name='foo')
        self.friend = get_user_model().objects.create_user(
            self.uni, 'friend@ucroo.com', name='Friend')
        self.notfriend = get_user_model().objects.create_user(
            self.uni, 'notfriend@ucroo.com', name='Not Friend')

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        # Student joins group (which auto-follows the group)
        group = Club.objects.create(user=self.notfriend, uni=self.uni, name='foo')
        ClubMember.objects.create(user=self.student, group=group)
        self.assertTrue(Follow.objects.is_following(self.student, group))
        # Friend also joined group
        ClubMember.objects.create(user=self.friend, group=group)
        # Student retrieves activity
        self.login(STUDENT)
        response = self.client.get(reverse('activity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Friend joined foo' in response.data['results'][0]['title'])
