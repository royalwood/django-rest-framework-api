from django.db import models
from model_utils.models import TimeStampedModel


class AppVersion(TimeStampedModel):
    dev = models.CharField(max_length=80, blank=True, null=True)
    stg = models.CharField(max_length=80, blank=True, null=True)
    prd = models.CharField(max_length=80, blank=True, null=True)
    iphone_version = models.CharField(max_length=20, null=True, blank=True)
    android_version = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return 'iPhone %s / Android %s' % (self.iphone_version, self.android_version)


class Category(TimeStampedModel):
    """Split this into marketplace and customgroup category models"""
    name = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
