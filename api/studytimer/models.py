from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

from universities.models import University
from subjects.models import Subject


class Entry(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    subject = models.ForeignKey(Subject, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    date = models.DateField()
    # Total minutes - remove this, should be a property calculated from
    # start/end times
    total_minutes = models.IntegerField(blank=True, null=True)
    # Active status - was previously named 'status'
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name
