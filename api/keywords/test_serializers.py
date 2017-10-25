from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .serializers import KeywordSerializer
from .models import Keyword


class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')
        self.user = get_user_model().objects.create_user(
            self.uni, 'foo@bar.com')

    def test(self):
        keyword = Keyword(user=self.user, uni=self.uni, word='Test')
        context = {'auth_user': self.user}
        serializer = KeywordSerializer(keyword, context=context)
        self.assertEqual(serializer.data['word'], 'Test')
