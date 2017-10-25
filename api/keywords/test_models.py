from django.test import TestCase
from django.contrib.auth import get_user_model

from universities.models import University
from .models import Keyword


PHONE_NUMBER = '+61437807666'

class Tests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(
            name='foo', phone_number=PHONE_NUMBER)
        self.user = get_user_model().objects.create_user(
            self.uni, 'user@ucroo.com')

    def test_string_representation(self):
        keyword = Keyword(user=self.user, uni=self.uni, word='test')
        self.assertEqual(str(keyword), keyword.word)

    def test_add_keyword(self):
        Keyword.objects.create(user=self.user, uni=self.uni, word='test')

    def test_get_keyword(self):
        Keyword.objects.create(user=self.user, uni=self.uni, word='test')
        keyword = Keyword.objects.get(word='test')
        self.assertEqual(keyword.word, 'test')

    def test_find_in(self):
        Keyword.objects.create(user=self.user, uni=self.uni, word='foo')
        Keyword.objects.create(user=self.user, uni=self.uni, word='bar')
        keywords = Keyword.objects.find_in('Testing foo testing')
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0].word, 'foo')

    def test_find_in_no_results(self):
        keywords = Keyword.objects.find_in('Testing')
        self.assertEqual(len(keywords), 0)

    def test_find_in_email_only(self):
        Keyword.objects.create(user=self.user, uni=self.uni, word='foo')
        Keyword.objects.create(user=self.user, uni=self.uni, word='bar', email=1)
        keywords = Keyword.objects.find_in('Testing bar testing', email=1)
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0].word, 'bar')

    def test_find_in_sms_only(self):
        Keyword.objects.create(user=self.user, uni=self.uni, word='foo')
        Keyword.objects.create(user=self.user, uni=self.uni, word='bar', sms=1)
        keywords = Keyword.objects.find_in('Testing bar testing', sms=1)
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0].word, 'bar')

    def test_render_body(self):
        body = Keyword.objects.render_body(
            'sms.txt', self.uni, [Keyword(word='foo')], 'http://test')
        self.assertGreater(len(body), 0)

    def test_render_sms(self):
        body = Keyword.objects.render_sms(
            self.uni, [Keyword(word='foo')], 'http://test')
        self.assertGreater(len(body), 0)

    def test_send_sms(self):
        # Need to mock Twilio so it doesn't keep sms-ing me
        #Keyword.objects.send_sms(PHONE_NUMBER, 'Hello tester')
        pass

    def test_notify_sms(self):
        Keyword.objects.create(
            user=self.user, uni=self.uni, word='foo', sms=True)
        # Need to mock twilio
        #Keyword.objects.notify_sms(self.uni, 'Hello foo', 'http://test')
