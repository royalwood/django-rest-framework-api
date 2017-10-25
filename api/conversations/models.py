from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class Conversation(TimeStampedModel):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return ' + '.join(self.members.values_list('name', flat=True))


class Message(TimeStampedModel):
    conversation = models.ForeignKey(Conversation)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    read = models.BooleanField(default=False)
