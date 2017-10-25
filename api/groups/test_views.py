"""Group View Tests"""
#pylint:disable=no-member
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from universities.models import University
from .models import (
    Club, ClubAdmin, ClubMember, CustomGroup, CustomGroupMember, StudentService,
    StudentServiceAdmin, StudentServiceMember, StudyGroup, StudyGroupMember,
    MentorGroup, MentorGroupMember)


USER_EMAIL = 'user@ucroo.com'
GROUPADMIN_EMAIL = 'groupadmin@ucroo.com'

class ClubTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = Club.objects.create(uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    # Get
    def test_get(self):
        """Any authenticated user can get groups"""
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:clubs-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_get_unauthenticated(self):
        """Only authenticated users can view groups"""
        response = self.client.get(reverse('api:clubs-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Get one
    def test_get_one(self):
        """Any authenticated user can get a group"""
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:clubs-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_unauthenticated(self):
        """Only authenticated users can view groups"""
        response = self.client.get(
            reverse('api:clubs-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_not_a_member_of(self):
        """Authenticated users can view a group they're not a member of"""
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:clubs-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Post
    def test_post(self):
        """Any authenticated user can add a group"""
        self.login(USER_EMAIL)
        data = {'name': 'Post Group'}
        response = self.client.post(reverse('api:clubs-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_unauthenticated(self):
        """Only authenticated users can post"""
        data = {'name': 'Post Group'}
        response = self.client.post(reverse('api:clubs-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Patch
    def test_patch(self):
        """Admins of a group can modify it"""
        self.login(GROUPADMIN_EMAIL)
        response = self.client.patch(
            reverse('api:clubs-detail', args=[self.group.pk]), {'name': 'Patch Group'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch Group')

    def test_patch_unauthenticated(self):
        """Unauthenticated users have no write access"""
        response = self.client.patch(
            reverse('api:clubs-detail', args=[self.group.pk]), {'name': 'Patch Group'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_not_an_admin(self):
        """Non-admins have no write access"""
        self.login(USER_EMAIL)
        response = self.client.patch(
            reverse('api:clubs-detail', args=[self.group.pk]), {'name': 'Patch Group'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Leave, Follow/unfollow feeds
    def test_leave(self):
        self.login(USER_EMAIL)
        response = self.client.post(
            reverse('api:clubs-leave', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow(self):
        self.login(USER_EMAIL)
        response = self.client.post(
            reverse('api:clubs-follow', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow(self):
        self.login(USER_EMAIL)
        response = self.client.post(
            reverse('api:clubs-unfollow', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CustomGroupTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.group = CustomGroup.objects.create(user=self.user, uni=self.uni)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:customgroups-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_get_suggested(self):
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:customgroups-list'), {'suggested': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one(self):
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:customgroups-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.login(USER_EMAIL)
        data = {'name': 'Post Group'}
        response = self.client.post(reverse('api:customgroups-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        self.login(USER_EMAIL)
        response = self.client.patch(
            reverse('api:customgroups-detail', args=[self.group.pk]), {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch group')


class StudentServiceTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = StudentService.objects.create(uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    # Get
    def test_get(self):
        """Any authenticated user can get group"""
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:studentservices-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_get_unauthenticated(self):
        """Only authenticated users can view studentservices"""
        response = self.client.get(reverse('api:studentservices-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Get one
    def test_get_one(self):
        """Any authenticated user can get a group"""
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studentservices-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_unauthenticated(self):
        """Only authenticated users can view studentservices"""
        response = self.client.get(
            reverse('api:studentservices-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_not_a_member_of(self):
        """Authenticated users can view a group they're not a member of"""
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studentservices-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Post
    def test_post(self):
        """Any authenticated user can add a group"""
        self.login(USER_EMAIL)
        data = {'name': 'Post Group'}
        response = self.client.post(reverse('api:studentservices-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_unauthenticated(self):
        """Only authenticated users can post"""
        data = {'name': 'Post Group'}
        response = self.client.post(reverse('api:studentservices-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Patch
    def test_patch(self):
        """Admins of a group can modify it"""
        self.login(GROUPADMIN_EMAIL)
        response = self.client.patch(
            reverse('api:studentservices-detail', args=[self.group.pk]), {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch group')

    def test_patch_unauthenticated(self):
        """Unauthenticated users have no write access"""
        response = self.client.patch(
            reverse('api:studentservices-detail', args=[self.group.pk]), {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_not_an_admin(self):
        """Non-admins have no write access"""
        self.login(USER_EMAIL)
        response = self.client.patch(
            reverse('api:studentservices-detail', args=[self.group.pk]), {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudyGroupTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from=timezone.now(),
            time_to=timezone.now(), time_day=1)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:studygroups-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_get_suggested(self):
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studygroups-list'), {'suggested': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one(self):
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studygroups-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.login(USER_EMAIL)
        data = {
            'name': 'Post Group',
            'time_from': '00:00:00',
            'time_to': '11:59:59',
            'time_day': 1,
        }
        response = self.client.post(reverse('api:studygroups-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        self.login(USER_EMAIL)
        response = self.client.patch(
            reverse('api:studygroups-detail', args=[self.group.pk]), {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch group')


class MentorGroupTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.group = MentorGroup.objects.create(uni=self.uni,
            user=self.user)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:mentorgroups-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_get_one(self):
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:mentorgroups-detail', args=[self.group.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.login(USER_EMAIL)
        data = {
            'name': 'Post Group',
        }
        response = self.client.post(reverse('api:mentorgroups-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        self.login(USER_EMAIL)
        url = reverse('api:mentorgroups-detail', args=[self.group.pk])
        response = self.client.patch(url, {'name': 'Patch group'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch group')


class ClubMemberTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = Club.objects.create(uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        ClubMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:clubmembers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_group(self):
        ClubMember.objects.create(user=self.user, group=self.group)
        # Add a second group with member
        group = Club.objects.create(uni=self.uni, user=self.groupadmin)
        ClubMember.objects.create(user=self.user, group=group)
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:clubmembers-list'), {'group': self.group.pk})
        self.assertEqual(response.data['count'], 1)

    def test_join(self):
        """Join a group"""
        self.login(USER_EMAIL)
        data = {
            'group': self.group.pk,
        }
        response = self.client.post(reverse('api:clubmembers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CustomGroupMemberTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = CustomGroup.objects.create(
            uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        CustomGroupMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:customgroupmembers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_group(self):
        CustomGroupMember.objects.create(user=self.user, group=self.group)
        # Add a second group with a member
        group = CustomGroup.objects.create(uni=self.uni, user=self.groupadmin)
        CustomGroupMember.objects.create(user=self.user, group=group)
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:customgroupmembers-list'), {'group': self.group.pk})
        self.assertEqual(response.data['count'], 1)

    def test_post(self):
        """Join a group"""
        self.login(USER_EMAIL)
        data = {
            'group': self.group.pk,
        }
        response = self.client.post(reverse('api:customgroupmembers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentServiceMemberTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = StudentService.objects.create(
            uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        StudentServiceMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:studentservicemembers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_group(self):
        StudentServiceMember.objects.create(user=self.user, group=self.group)
        # Add a second group with a member
        group = StudentService.objects.create(uni=self.uni, user=self.groupadmin)
        StudentServiceMember.objects.create(user=self.user, group=group)
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studentservicemembers-list'), {'group': self.group.pk})
        self.assertEqual(response.data['count'], 1)

    def test_post(self):
        """Join a group"""
        self.login(USER_EMAIL)
        data = {
            'group': self.group.pk,
        }
        response = self.client.post(reverse('api:studentservicemembers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudyGroupMemberTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        StudyGroupMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:studygroupmembers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_group(self):
        StudyGroupMember.objects.create(user=self.user, group=self.group)
        # Add a second group with a member
        group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1)
        StudyGroupMember.objects.create(user=self.user, group=group)
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:studygroupmembers-list'), {'group': self.group.pk})
        self.assertEqual(response.data['count'], 1)

    def test_post(self):
        """Join a group"""
        self.login(USER_EMAIL)
        data = {
            'group': self.group.pk,
        }
        response = self.client.post(reverse('api:studygroupmembers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MentorGroupMemberTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = MentorGroup.objects.create(user=self.user, uni=self.uni)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        MentorGroupMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('api:mentorgroupmembers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_group(self):
        MentorGroupMember.objects.create(user=self.user, group=self.group)
        # Add a second group with a member
        group = MentorGroup.objects.create(user=self.user, uni=self.uni)
        MentorGroupMember.objects.create(user=self.user, group=group)
        self.login(USER_EMAIL)
        response = self.client.get(
            reverse('api:mentorgroupmembers-list'), {'group': self.group.pk})
        self.assertEqual(response.data['count'], 1)

    def test_post(self):
        """Join a group"""
        self.login(USER_EMAIL)
        data = {
            'group': self.group.pk,
        }
        response = self.client.post(reverse('api:mentorgroupmembers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class JoinedGroupsTests(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(self.uni, USER_EMAIL)
        self.groupadmin = get_user_model().objects.create_user(
            self.uni, GROUPADMIN_EMAIL)
        self.group = Club.objects.create(uni=self.uni, user=self.groupadmin)

    def login(self, username, password='ucroo123'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Could not login')

    def test_get(self):
        # User joins the group
        ClubMember.objects.create(user=self.user, group=self.group)
        self.login(USER_EMAIL)
        response = self.client.get(reverse('joinedgroups'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['clubs']), 0)
