"""
Someone posted in group
Someone commented on your post
Someone also commented
Connection joined group
Connection posted in marketplace
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from actstream.actions import follow
from actstream.models import user_stream

from universities.models import University
from core.models import Category
from marketplace.models import Item
from groups.models import Club, ClubMember
from feeds.models import Post, Comment
from actstream.models import Follow
from users.models import Connection


class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.student = get_user_model().objects.create_user(
            self.uni, 'student@ucroo.com', name='Student')
        self.friend = get_user_model().objects.create_user(
            self.uni, 'friend@ucroo.com', name='Friend')
        self.notfriend = get_user_model().objects.create_user(
            self.uni, 'notfriend@ucroo.com', name='Not Friend')

    def test_someone_posted_in_group(self):
        group = Club.objects.create(user=self.notfriend, uni=self.uni, name='foo')
        # Student joins group (which auto-follows the group)
        ClubMember.objects.create(user=self.student, group=group)
        self.assertTrue(Follow.objects.is_following(self.student, group))
        # Friend posts in group
        Post.objects.create(
            user=self.notfriend, uni=self.uni, feed_object='club',
            feed_object_id=group.pk, title='bar')
        # Student gets activity
        activity = user_stream(self.student)
        self.assertTrue('Not Friend posted bar on foo' in str(activity.first()))

    def test_someone_commented_on_your_post(self):
        # Student makes a post (which auto-follows the post)
        post = Post.objects.create(
            user=self.student, uni=self.uni, feed_object='university',
            feed_object_id=self.uni.pk, title='foo')
        self.assertTrue(Follow.objects.is_following(self.student, post))
        # Friend comments on the post
        Comment.objects.create(user=self.friend, post=post, text='bar')
        # Student gets activity
        activity = user_stream(self.student)
        self.assertTrue('Friend commented bar on foo' in str(activity.first()))

    def test_someone_also_commented(self):
        # Not Friend makes a post
        post = Post.objects.create(
            user=self.notfriend, uni=self.uni, feed_object='university',
            feed_object_id=self.uni.pk, title='foo')
        # Student comments on the post (which auto-follows the post)
        Comment.objects.create(user=self.student, post=post, text='foo')
        self.assertTrue(Follow.objects.is_following(self.student, post))
        # Not Friend also comments
        Comment.objects.create(user=self.notfriend, post=post, text='bar')
        # Student gets activity
        activity = user_stream(self.student)
        self.assertTrue('Not Friend commented bar on foo' in str(activity.first()))

    def test_connection_joined_group(self):
        group = Club.objects.create(user=self.notfriend, uni=self.uni, name='foo')
        # Student joins group (which auto-follows the group)
        ClubMember.objects.create(user=self.student, group=group)
        self.assertTrue(Follow.objects.is_following(self.student, group))
        # Friend also joined group
        ClubMember.objects.create(user=self.friend, group=group)
        # Student gets activity
        activity = user_stream(self.student)
        self.assertTrue('Friend joined foo' in str(activity.first()))

    def test_connection_posted_in_marketplace(self):
        # Student connects to Friend (which auto-follow the friend)
        self.student.add_connection(self.friend)
        # Friend posts a marketplace item
        category = Category.objects.create(name='Test', module='marketplace')
        Item.objects.create(
            user=self.friend, title='foo', price='10.00', category=category)
        # Student gets activity
        activity = user_stream(self.student)
        self.assertTrue('Friend posted marketplace item foo' in str(activity.first()))
