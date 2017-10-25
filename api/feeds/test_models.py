from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import Post, Comment, PostLog


class PostTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'user@ucroo.com')

    def test_body_plain(self):
        post = Post(user=self.user, uni=self.uni, body='<html>Text</html>')
        self.assertEqual(post.body_plain, 'Text')

    def test_body_markdown(self):
        post = Post(user=self.user, uni=self.uni, body='<html>Text</html>')
        self.assertEqual(post.body_markdown, "Text\n\n")

    def test_body_html(self):
        post = Post(user=self.user, uni=self.uni, body='<html>Text</html>')
        self.assertEqual(post.body_html, '<html>Text</html>')

    def test_status_posted(self):
        post = Post(user=self.user, uni=self.uni, body='foo')
        self.assertEqual(post.status, Post.STATUS.posted)

    def test_status_reported(self):
        """Ensure a post's status is set to reported, if a report is logged"""
        post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')
        post.report(self.user)
        self.assertEqual(post.status, Post.STATUS.reported)

    def test_status_cleared(self):
        """Ensure a post's status is set to reported, if a report is logged"""
        post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')
        post.clear(self.user)
        self.assertEqual(post.status, Post.STATUS.cleared)


class CommentTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'user@ucroo.com')
        self.post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')

    def test_count(self):
        Comment.objects.create(user=self.user, post=self.post, text='foo')
        total = Comment.objects.count(self.post)
        self.assertEqual(total, 1)


class PostLogTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'user@ucroo.com')
        self.post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')

    def test_posted(self):
        post_log = PostLog.objects.all().first()
        self.assertEqual(post_log.status, Post.STATUS.posted)

    def test_edited(self):
        self.post.body = 'bar'
        self.post.save()
        post_log = PostLog.objects.all().last()
        self.assertEqual(post_log.status, Post.STATUS.posted)

    def test_reported(self):
        post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')
        post.report(self.user)
        post_log = Post.objects.all().last()
        self.assertEqual(post_log.status, Post.STATUS.reported)

    def test_cleared(self):
        post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')
        post.clear(self.user)
        post_log = Post.objects.all().last()
        self.assertEqual(post_log.status, Post.STATUS.cleared)
