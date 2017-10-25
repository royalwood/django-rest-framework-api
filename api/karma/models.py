from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class Incentive(TimeStampedModel):
    description = models.CharField(max_length=250)
    percentage_points = models.SmallIntegerField()
    action_url = models.CharField(max_length=250)

    def __str__(self):
        return self.description

class History(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    points = models.SmallIntegerField()
    points_type = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return "%s, %s points" % (self.user.name, self.points)


class Type(TimeStampedModel):
    description = models.CharField(max_length=250)
    points = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.description
