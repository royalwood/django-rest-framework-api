"""Group Serializer Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import (
    Club, ClubMember, CustomGroup, CustomGroupMember, StudentService,
    StudentServiceMember, StudyGroup, StudyGroupMember, MentorGroup,
    MentorGroupMember)
from .serializers import (
    ClubSerializer, ClubMemberSerializer, CustomGroupSerializer,
    CustomGroupMemberSerializer, StudentServiceSerializer,
    StudentServiceMemberSerializer, StudyGroupSerializer,
    StudyGroupMemberSerializer, MentorGroupSerializer,
    MentorGroupMemberSerializer)


class ClubTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = Club.objects.create(
            user=self.user, uni=self.uni, name='foo')

    def test(self):
        serializer = ClubSerializer(self.group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['name'], 'foo')


class ClubMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = Club.objects.create(
            user=self.user, uni=self.uni, name='foo')
        self.member = ClubMember.objects.create(
            user=self.user, group=self.group)

    def test(self):
        context = {'auth_user': self.user}
        serializer = ClubMemberSerializer(self.member, context=context)
        self.assertEqual(serializer.data['user']['email'], 'foo@bar.com')


class CustomGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = CustomGroup.objects.create(
            user=self.user, uni=self.uni, name='foo')
        self.member = CustomGroupMember.objects.create(
            user=self.user, group=self.group)

    def test(self):
        context = {'auth_user': self.user}
        serializer = CustomGroupMemberSerializer(self.member, context=context)
        self.assertEqual(serializer.data['user']['email'], 'foo@bar.com')


class StudentServiceTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = StudentService.objects.create(
            user=self.user, uni=self.uni, name='foo')

    def test(self):
        serializer = StudentServiceSerializer(
            self.group, context={'auth_user': self.user})
        self.assertEqual(serializer.data['name'], 'foo')


class StudentServiceMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = StudentService.objects.create(
            user=self.user, uni=self.uni, name='foo')
        self.member = StudentServiceMember.objects.create(
            user=self.user, group=self.group)

    def test(self):
        serializer = StudentServiceMemberSerializer(
            self.member, context={'auth_user': self.user})
        self.assertEqual(serializer.data['user']['email'], 'foo@bar.com')


class StudyGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1, name='foo')
        self.member = StudyGroupMember.objects.create(
            user=self.user, group=self.group)

    def test(self):
        serializer = StudyGroupMemberSerializer(
            self.member, context={'auth_user': self.user})
        self.assertEqual(serializer.data['user']['email'], 'foo@bar.com')


class MentorGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, email='foo@bar.com')
        self.group = MentorGroup.objects.create(
            user=self.user, uni=self.uni, name='foo')
        self.member = MentorGroupMember.objects.create(
            user=self.user, group=self.group)

    def test(self):
        serializer = MentorGroupMemberSerializer(
            self.member, context={'auth_user': self.user})
        self.assertEqual(serializer.data['user']['email'], 'foo@bar.com')
