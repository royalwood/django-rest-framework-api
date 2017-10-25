from django.core.validators import RegexValidator
from django.db import models
from model_utils.models import TimeStampedModel


message = 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=message)

class University(TimeStampedModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=255)
    code = models.CharField(max_length=5)
    state = models.CharField(max_length=255)
    policy = models.TextField(blank=True, null=True)
    sign_up = models.BooleanField(default=True)

    # Phone number - merged from the old alert_number. Used to send notification
    # sms messages when keywords match a post.
    phone_number = models.CharField(max_length=16, validators=[phone_regex], blank=True)

    # Secret keys use for integrations
    aaf = models.BooleanField(default=False)
    aff_token = models.CharField(max_length=255, blank=True, null=True)
    app_key = models.CharField(max_length=255, blank=True, null=True)
    secret_key = models.CharField(max_length=255, blank=True, null=True)

    # Merged in from UniversityLti
    lti_key = models.CharField(max_length=255, null=True)
    lti_secret = models.CharField(max_length=255, null=True)
    lti_context_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Campus(TimeStampedModel):
    uni = models.ForeignKey(University)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True, null=True)
    timezone = models.CharField(max_length=300)
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class School(TimeStampedModel):
    uni = models.ForeignKey(University)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '%s (%s)' % (self.name, self.uni)


class Course(TimeStampedModel):
    uni = models.ForeignKey(University)
    name = models.CharField(max_length=100)
    # "it should be optional to provide the course code" - Chase
    code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
