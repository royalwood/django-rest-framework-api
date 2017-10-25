from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import Conversation, Message


class ConversationTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, 'student@ucroo.com', name='Student')
        self.friend = get_user_model().objects.create_user(
            self.uni, 'friend@ucroo.com', name='Friend')

    def test_create(self):
        conversation = Conversation.objects.create()
        conversation.members.add(self.student, self.friend)
        conversation.save()

    def test_string_representation(self):
        conversation = Conversation.objects.create()
        conversation.members.add(self.student, self.friend)
        self.assertEqual(str(conversation), 'Student + Friend')


class MessageTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, 'student@ucroo.com', name='Student')
        self.friend = get_user_model().objects.create_user(
            self.uni, 'friend@ucroo.com', name='Friend')

    def test_create(self):
        conversation = Conversation.objects.create()
        message = Message.objects.create(
            user=self.student, conversation=conversation, text='foo')
