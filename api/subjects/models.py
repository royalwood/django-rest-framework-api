from django.db import models
from django.db.models import Q
from django.conf import settings
from model_utils.models import TimeStampedModel

from universities.models import University, Campus


class SubjectManager(models.Manager):
    def search(self, query):
        return self.filter(
            Q(name__icontains=query) | Q(subject_title__icontains=query))


class Subject(TimeStampedModel):
    uni = models.ForeignKey(University)
    # User who added the subject (was added_user)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    # Code is required. "subjects will always have a code" - Chase.
    code = models.CharField(max_length=21)
    # The following were merged from UnitInfoData
    added_user_type = models.CharField(max_length=25)
    subject_title = models.CharField(max_length=250, blank=True, null=True)
    subject_type = models.CharField(max_length=250, blank=True, null=True)
    activity_number = models.CharField(max_length=25, blank=True, null=True)
    campus = models.ForeignKey(Campus, null=True)
    class_type = models.CharField(max_length=25, blank=True, null=True)
    day = models.CharField(max_length=10, blank=True, null=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    location = models.CharField(max_length=25, blank=True, null=True)
    # search - remove this. Pointless.
    search = models.CharField(max_length=150, null=True)
    semester = models.CharField(max_length=255)
    staff = models.CharField(max_length=250, blank=True, null=True)
    time = models.TimeField(null=True)
    year = models.IntegerField(null=True)

    objects = SubjectManager()

    def __str__(self):
        return self.name


# Rename this to just Enrollee
class SubjectEnrollee(TimeStampedModel):
    """Student enrolled in a subject"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_ucroo_id = models.IntegerField(blank=True, null=True)
    subject = models.ForeignKey(Subject)
    semester = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()

    def __str__(self):
        return '%s enrolled in %s' % (self.user.name, self.subject.code)


# Rename this to Tag
class SubjectTag(TimeStampedModel):
    """Was feed_tags, but was only being used for subject tags, so renaming."""
    feed_object = models.CharField(max_length=16)
    feed_object_id = models.IntegerField()
    title = models.CharField(max_length=300)
    sort_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
