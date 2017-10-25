from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

class FileUpload(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False)
    object_id = models.IntegerField(blank=True, null=True)
    filename = models.CharField(max_length=80, blank=True, null=True)
    file_size = models.IntegerField(default=0, null=False, blank=True)

    def __str__(self):
        return '%s uploaded by %s (%s kb)' % (self.filename, self.user, self.file_size)
