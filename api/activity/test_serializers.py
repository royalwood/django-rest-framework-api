"""Convert this to serializer tests! No need to test the views"""
#pylint:disable=no-member
from django.test import TestCase
from django.contrib.auth import get_user_model
from actstream.models import user_stream

from universities.models import University
from groups.models import Club, ClubMember
from feeds.models import Post, Comment
from feeds.settings import FEED_OBJECT_TYPES
from marketplace.models import Item
from core.models import Category
from users.models import Connection
from .serializers import ActivitySerializer


STUDENT = 'student@ucroo.com'
FRIEND = 'friend@ucroo.com'

class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_superuser(
            self.uni, STUDENT, name='Student')
        self.friend = get_user_model().objects.create_user(
            self.uni, FRIEND, name='Friend')
        self.student.add_connection(self.friend)

    def test_someone_posted_in_group(self):
        """Someone posted in a group the user is in"""
        # Student is member of a group
        club = Club.objects.create(user=self.student, uni=self.uni, name='foo')
        ClubMember.objects.create(user=self.student, group=club)
        # Friend posts in the group
        Post.objects.create(
            user=self.friend, uni=self.uni,
            feed_object=FEED_OBJECT_TYPES['CLUBS'], feed_object_id=club.pk,
            title='bar')
        # Student retrieves activity
        activity = user_stream(self.student)
        context = {'auth_user': self.student}
        serializer = ActivitySerializer(activity.first(), context=context)
        self.assertTrue('Friend posted bar on foo' in serializer.data['title'])

    def test_someone_commented_on_your_post(self):
        """Someone comments on user's post (group or marketplace post)"""
        # Student creates a Club post
        club = Club.objects.create(user=self.student, uni=self.uni, name='foo')
        ClubMember.objects.create(user=self.student, group=club)
        post = Post.objects.create(
            user=self.student, uni=self.uni,
            feed_object=FEED_OBJECT_TYPES['CLUBS'], feed_object_id=club.pk,
            title='foo')
        # Friend comments on the post
        Comment.objects.create(user=self.friend, post=post, text='bar')
        # Student retrieves activity
        activity = user_stream(self.student)
        context = {'auth_user': self.student}
        serializer = ActivitySerializer(activity.first(), context=context)
        self.assertTrue('Friend commented bar on foo' in serializer.data['title'])

    def test_someone_also_commented(self):
        """Someone comments on a post the user also commented on (group or
        marketplace)
        """
        # Student comments on a post
        post = Post.objects.create(
            user=self.friend, uni=self.uni,
            feed_object=FEED_OBJECT_TYPES['ALLSTUDENTS'],
            feed_object_id=self.uni.pk, title='foo')
        Comment.objects.create(user=self.student, post=post, text='foo')
        # Friend also comments
        Comment.objects.create(user=self.friend, post=post, text='bar')
        # Student retrieves activity
        activity = user_stream(self.student)
        context = {'auth_user': self.student}
        serializer = ActivitySerializer(activity.first(), context=context)
        self.assertTrue('Friend commented bar on foo' in serializer.data['title'])

    def test_connection_posted_in_marketplace(self):
        """A connection is selling/wanting an item in the Marketplace."""
        # Friend sells an item
        category = Category.objects.create(name='foo', module='marketplace')
        item = Item.objects.create(
            user=self.friend, category=category, title='foo', price=10.00)
        # Student retrieves activity
        activity = user_stream(self.student)
        context = {'auth_user': self.student}
        serializer = ActivitySerializer(activity.first(), context=context)
        self.assertTrue('Friend posted marketplace item foo' in serializer.data['title'])

    def test_connection_joined_group(self):
        """A connection joined/followed a group - does NOT include private study
        groups, private custom groups, mentor groups AND is NOT triggered if
        connection is added to group by another user
        """
        # Student joins group
        group = Club.objects.create(user=self.student, uni=self.uni, name='foo')
        ClubMember.objects.create(user=self.student, group=group)
        # Friend also joins group
        ClubMember.objects.create(user=self.friend, group=group)
        # Student retrieves activity
        activity = user_stream(self.student)
        context = {'auth_user': self.student}
        serializer = ActivitySerializer(activity.first(), context=context)
        self.assertTrue('Friend joined foo' in serializer.data['title'])
