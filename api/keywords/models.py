from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from model_utils.models import TimeStampedModel
from twilio.rest import TwilioRestClient

from universities.models import University
from subjects.models import Subject


class KeywordManager(models.Manager):
    use_for_related_fields = True

    def find_in(self, text, **kwargs):
        """Returns all keywords that exist in `text`"""
        # Get all keywords
        if kwargs:
            try:
                keywords = self.filter(**kwargs)
            except Keyword.DoesNotExist:
                return []
        else:
            keywords = self.all()
        # Remove all keywords that don't exist in `text`
        keywords = [k for k in keywords if k.word.lower() in text.lower()]
        return keywords

    @staticmethod
    def render_body(template_filename, uni, keywords, link):
        """Returns a string rendered from template_filename"""
        template = get_template(template_filename)
        # Comma-separate the list of words
        words = ', '.join([k.word for k in keywords])
        context = Context({'uni': uni, 'words': words, 'link': link})
        return template.render(context)

    @classmethod
    def render_sms(cls, uni, keywords, link):
        return cls.render_body('sms.txt', uni, keywords, link)

    @classmethod
    def render_email(cls, uni, keywords, link):
        return cls.render_body('email.txt', uni, keywords, link)

    @staticmethod
    def send_sms(phone_number, body):
        """Send an sms via Twilio API. Should move this to another module
        somewhere to make it reusable.
        """
        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body, from_=settings.TWILIO_FROM, to=phone_number)

    def notify_sms(self, uni, text, link):
        keywords = self.find_in(text, sms=True)
        if keywords:
            body = self.render_sms(uni, keywords, link)
            self.send_sms(uni.phone_number, body)

    def notify_email(self, uni, text, link):
        keywords = self.find_in(text, email=True)
        if keywords:
            body = self.render_email(uni, keywords, link)
            # Emails aren't done yet
            #send_email(uni.phone_number, body)

    def notify(self, uni, text, link):
        """Sends both sms and email if keywords found in `text`"""
        self.notify_sms(uni, text, link)
        self.notify_email(uni, text, link)


class Keyword(TimeStampedModel):
    uni = models.ForeignKey(University, related_name='keywords')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='keywords')
    subject = models.ForeignKey(Subject, null=True, related_name='keywords')
    email = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    notify_all = models.BooleanField(default=False)
    word = models.CharField(max_length=40)

    objects = KeywordManager()

    def save(self, *args, **kwargs):
        if self.word:
            self.word = self.word.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('word',)
