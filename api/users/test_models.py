from django.test import TestCase

from universities.models import University
from actstream.models import Follow
from .models import User, BlockedUser, Connection


class UserTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')

    def test_add_user(self):
        User.objects.create_user(self.uni, 'user@ucroo.com')


class ConnectionTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = User.objects.create_user(
            self.uni, 'student@ucroo.com', name='Student')
        self.friend = User.objects.create_user(
            self.uni, 'friend@ucroo.com', name='Friend')

    def test_request_connection(self):
        self.student.add_connection(self.friend)
        # Student's connection status
        self.assertEqual(self.student.total_pending_connections, 0)
        self.assertEqual(self.student.total_requested_connections, 1)
        self.assertEqual(self.student.total_accepted_connections, 0)
        self.assertEqual(self.student.total_blocked_connections, 0)
        self.assertFalse(self.student.is_connected(self.friend))
        self.assertTrue(Follow.objects.is_following(self.student, self.friend))
        # Friend's connection status
        self.assertEqual(self.friend.total_pending_connections, 1)
        self.assertEqual(self.friend.total_requested_connections, 0)
        self.assertEqual(self.friend.total_accepted_connections, 0)
        self.assertEqual(self.friend.total_blocked_connections, 0)
        self.assertFalse(self.friend.is_connected(self.student))
        self.assertFalse(Follow.objects.is_following(self.friend, self.student))

    def test_accept_connection(self):
        # Request connection with Friend
        self.student.add_connection(self.friend)
        # Friend accepts the request
        self.friend.add_connection(self.student)
        # Student's connection status
        self.assertEqual(self.student.total_pending_connections, 0)
        self.assertEqual(self.student.total_requested_connections, 0)
        self.assertEqual(self.student.total_accepted_connections, 1)
        self.assertEqual(self.student.total_blocked_connections, 0)
        self.assertTrue(self.student.is_connected(self.friend))
        self.assertTrue(Follow.objects.is_following(self.student, self.friend))
        # Friend's connection status
        self.assertEqual(self.friend.total_pending_connections, 0)
        self.assertEqual(self.friend.total_requested_connections, 0)
        self.assertEqual(self.friend.total_accepted_connections, 1)
        self.assertEqual(self.friend.total_blocked_connections, 0)
        self.assertTrue(self.friend.is_connected(self.student))
        self.assertTrue(Follow.objects.is_following(self.friend, self.student))

    def test_block_connection(self):
        # Request connection with Friend
        self.student.add_connection(self.friend)
        # Friend blocks student
        self.friend.block_connection(self.student)
        # Student's connection status
        self.assertEqual(self.student.total_pending_connections, 0)
        self.assertEqual(self.student.total_requested_connections, 1)
        self.assertEqual(self.student.total_accepted_connections, 0)
        self.assertEqual(self.student.total_blocked_connections, 0)
        self.assertFalse(self.student.is_connected(self.friend))
        self.assertTrue(Follow.objects.is_following(self.student, self.friend))
        # Friend's connection status
        self.assertEqual(self.friend.total_pending_connections, 0)
        self.assertEqual(self.friend.total_requested_connections, 0)
        self.assertEqual(self.friend.total_accepted_connections, 0)
        self.assertEqual(self.friend.total_blocked_connections, 1)
        self.assertFalse(self.friend.is_connected(self.student))
        self.assertFalse(Follow.objects.is_following(self.friend, self.student))

    def test_remove_connection(self):
        # Request connection with Friend
        self.student.add_connection(self.friend)
        # Accept the request
        self.friend.add_connection(self.student)
        # Remove connection
        self.student.remove_connection(self.friend)
        # Student's connection status
        self.assertEqual(self.student.total_pending_connections, 0)
        self.assertEqual(self.student.total_requested_connections, 0)
        self.assertEqual(self.student.total_accepted_connections, 0)
        self.assertEqual(self.student.total_blocked_connections, 0)
        self.assertFalse(self.student.is_connected(self.friend))
        self.assertFalse(Follow.objects.is_following(self.student, self.friend))
        # Friend's connection status
        self.assertEqual(self.friend.total_pending_connections, 0)
        self.assertEqual(self.friend.total_requested_connections, 0)
        self.assertEqual(self.friend.total_accepted_connections, 0)
        self.assertEqual(self.friend.total_blocked_connections, 0)
        self.assertFalse(self.friend.is_connected(self.friend))
        # Friend should continue following
        self.assertTrue(Follow.objects.is_following(self.friend, self.student))

    def test_connection_status_disconnected(self):
        status = self.student.get_connection_status(self.friend)
        self.assertEqual(status, 'disconnected')

    def test_connection_status_pending(self):
        self.friend.add_connection(self.student)
        status = self.student.get_connection_status(self.friend)
        self.assertEqual(status, 'pending')

    def test_connection_status_pending(self):
        self.friend.add_connection(self.student)
        status = self.student.get_connection_status(self.friend)
        self.assertEqual(status, 'pending')

    def test_connection_status_requested(self):
        self.student.add_connection(self.friend)
        status = self.student.get_connection_status(self.friend)
        self.assertEqual(status, 'requested')

    def test_connection_status_blocked(self):
        self.student.block_connection(self.friend)
        status = self.student.get_connection_status(self.friend)
        self.assertEqual(status, 'blocked')
