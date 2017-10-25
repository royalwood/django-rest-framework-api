from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .serializers import PostSerializer
from .models import Post, Comment


class PostTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'test@ucroo.com')

    def test(self):
        post = Post(user=self.user, body='<html>Text</html>')
        context = {'auth_user': self.user}
        serializer = PostSerializer(post, context=context)
        self.assertEqual(serializer.data['body'], '<html>Text</html>')

    def test_fmt_plain(self):
        post = Post(user=self.user, body='<html>Text</html>')
        context = {'auth_user': self.user, 'fmt': 'plain'}
        serializer = PostSerializer(post, context=context)
        self.assertEqual(serializer.data['body'], 'Text')

    def test_comments(self):
        post = Post.objects.create(
            user=self.user, uni=self.uni, feed_object='university',
            feed_object_id=1, body='foo')
        Comment.objects.create(user=self.user, post=post, text='foo')
        context = {'auth_user': self.user}
        serializer = PostSerializer(post, context=context)
        self.assertEqual(serializer.data['comments'][0]['text'], 'foo')
        self.assertEqual(serializer.data['total_comments'], 1)
