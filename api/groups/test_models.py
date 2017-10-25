from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import (
    Club, ClubAdmin, ClubMember, CustomGroup, CustomGroupMember, StudentService,
    StudentServiceAdmin, StudentServiceMember, StudyGroup, StudyGroupMember,
    MentorGroup, MentorGroupMember)


class ClubTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(uni=self.uni)
        self.group = Club.objects.create(user=self.user, uni=self.uni)

    # Admins
    def test_add_admin(self):
        self.group.remove_admin(self.user)
        self.assertFalse(self.group.is_admin(self.user))
        self.group.add_admin(self.user)
        self.assertTrue(self.group.is_admin(self.user))

    def test_add_admin_twice(self):
        self.group.add_admin(self.user)
        self.group.add_admin(self.user)
        self.assertTrue(self.group.is_admin(self.user))
        self.assertEqual(self.group.total_admins, 1)

    def test_remove_admin(self):
        self.group.remove_admin(self.user)
        self.assertFalse(self.group.is_admin(self.user))

    def test_total_admins(self):
        # Should have one, because the user who created the group should be
        # added as admin
        self.assertEqual(self.group.total_admins, 1)

    def test_is_admin(self):
        self.assertTrue(self.group.is_admin(self.user))

    # Members
    def test_remove_member(self):
        ClubMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))
        self.group.remove_member(self.user)
        self.assertFalse(self.group.is_member(self.user))

    def test_is_member(self):
        ClubMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))

    def test_total_members(self):
        self.assertEqual(self.group.total_members, 0)

    def test_total_followers(self):
        # Should have one, because creators are set to auto-follow
        self.assertEqual(self.group.total_followers, 1)


class CustomGroupTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(uni=self.uni)
        self.group = CustomGroup.objects.create(user=self.user, uni=self.uni)

    # Admin (Customgroups don't have admins)
    def test_add_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.add_admin(self.user)

    def test_remove_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.remove_admin(self.user)

    def test_is_admin(self):
        self.assertFalse(self.group.is_admin(self.user))

    def test_total_admins(self):
        self.assertEqual(self.group.total_admins, 0)

    # Member
    def test_remove_member(self):
        CustomGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))
        self.group.remove_member(self.user)
        self.assertFalse(self.group.is_member(self.user))

    def test_is_member(self):
        CustomGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))

    def test_total_members(self):
        self.assertEqual(self.group.total_members, 0)


class StudentServiceTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(uni=self.uni)
        self.group = StudentService.objects.create(user=self.user, uni=self.uni)

    # Admins
    def test_add_admin(self):
        self.group.add_admin(self.user)
        self.assertTrue(self.group.is_admin(self.user))

    def test_add_admin_twice(self):
        self.group.add_admin(self.user)
        self.group.add_admin(self.user)
        self.assertEqual(self.group.total_admins, 1)

    def test_remove_admin(self):
        self.group.remove_admin(self.user)
        self.assertFalse(self.group.is_admin(self.user))

    def test_is_admin(self):
        StudentServiceAdmin.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_admin(self.user))

    def test_total_admins(self):
        # Should have one, because the user who created the group should be
        # added as admin
        self.assertEqual(self.group.total_admins, 1)

    # Members
    def test_remove_member(self):
        StudentServiceMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))
        self.group.remove_member(self.user)
        self.assertFalse(self.group.is_member(self.user))

    def test_is_member(self):
        StudentServiceMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))

    def test_total_members(self):
        self.assertEqual(self.group.total_members, 0)


class StudyGroupTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(uni=self.uni)
        self.group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1)

    # Admin (Studygroups don't have admins)
    def test_add_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.add_admin(self.user)

    def test_remove_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.remove_admin(self.user)

    def test_is_admin(self):
        self.assertFalse(self.group.is_admin(self.user))

    def test_total_admins(self):
        self.assertEqual(self.group.total_admins, 0)

    # Member
    def test_remove_member(self):
        StudyGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))
        self.group.remove_member(self.user)
        self.assertFalse(self.group.is_member(self.user))

    def test_is_member(self):
        StudyGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))

    def test_total_members(self):
        self.assertEqual(self.group.total_members, 0)


class MentorGroupTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(uni=self.uni)
        self.group = MentorGroup.objects.create(user=self.user, uni=self.uni)

    # Admins (Mentor groups don't have admins)
    def test_add_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.add_admin(self.user)

    def test_remove_admin(self):
        with self.assertRaises(NotImplementedError):
            self.group.remove_admin(self.user)

    def test_is_admin(self):
        self.assertFalse(self.group.is_admin(self.user))

    def test_total_admins(self):
        self.assertEqual(self.group.total_admins, 0)

    # Members
    def test_remove_member(self):
        MentorGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))
        self.group.remove_member(self.user)
        self.assertFalse(self.group.is_member(self.user))

    def test_is_member(self):
        MentorGroupMember.objects.create(user=self.user, group=self.group)
        self.assertTrue(self.group.is_member(self.user))

    def test_total_members(self):
        self.assertEqual(self.group.total_members, 0)


class ClubMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(
            uni=self.uni, name='foo')
        self.group = Club.objects.create(user=self.user, uni=self.uni)

    def test_string_representation(self):
        member = ClubMember(user=self.user, group=self.group)
        self.assertEqual(str(member), 'foo')

    def test_add(self):
        ClubMember(user=self.user, group=self.group)


class CustomGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(
            uni=self.uni, name='foo')
        self.group = CustomGroup.objects.create(user=self.user, uni=self.uni)

    def test_string_representation(self):
        member = CustomGroupMember(user=self.user, group=self.group)
        self.assertEqual(str(member), 'foo')

    def test_add(self):
        CustomGroupMember(user=self.user, group=self.group)


class StudentServiceMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(
            uni=self.uni, name='foo')
        self.group = StudentService.objects.create(user=self.user, uni=self.uni)

    def test_string_representation(self):
        member = StudentServiceMember(user=self.user, group=self.group)
        self.assertEqual(str(member), 'foo')

    def test_add(self):
        StudentServiceMember(user=self.user, group=self.group)


class StudyGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(
            uni=self.uni, name='foo')
        self.group = StudyGroup.objects.create(
            user=self.user, uni=self.uni, time_from='00:00:00',
            time_to='11:59:59', time_day=1)

    def test(self):
        StudyGroupMember(user=self.user, group=self.group)

    def test_string_representation(self):
        member = StudyGroupMember(user=self.user, group=self.group)
        self.assertEqual(str(member), 'foo')


class MentorGroupMemberTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create(
            uni=self.uni, name='foo')
        self.group = MentorGroup.objects.create(user=self.user, uni=self.uni)

    def test(self):
        MentorGroupMember(user=self.user, group=self.group)

    def test_string_representation(self):
        member = MentorGroupMember(user=self.user, group=self.group)
        self.assertEqual(str(member), 'foo')
