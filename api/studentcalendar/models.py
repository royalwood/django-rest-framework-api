from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

from subjects.models import Subject


class Calendar(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True)
#    unit_info = models.ForeignKey(UnitInfoData, blank=True, null=True)
    type = models.CharField(max_length=12)
    class_type = models.CharField(max_length=50)
    title = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    time_day = models.IntegerField()
    is_all_day_event = models.BooleanField(default=False)
    color = models.CharField(max_length=200, blank=True, null=True)
    by_academic = models.IntegerField(blank=True, null=True)
    recurring_rule = models.CharField(max_length=11, blank=True, null=True)
    assessment_date = models.DateField(blank=True, null=True)
    assessment_time = models.TimeField(blank=True, null=True)
    assessment_alert = models.DateField(blank=True, null=True)
    event_cal_type = models.CharField(max_length=1)

    def __str__(self):
        return "'%s' cal event by %s" % (self.title, self.user.name)
