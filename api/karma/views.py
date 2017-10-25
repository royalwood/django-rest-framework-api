from django.db.models.signals import post_save

from subjects.models import SubjectEnrollee
from .models import History


# add karma points on create
def add_subject_karma_points(sender, instance, **kwargs): #pylint:disable=unused-argument
    if kwargs['created']:
        obj = History.objects.create(user=instance.user, points=5, points_type=None,
                                                description='subject added')
        obj.save()

post_save.connect(add_subject_karma_points, sender=SubjectEnrollee)
post_save.disconnect(add_subject_karma_points)
