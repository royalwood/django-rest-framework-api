"""Activity Views"""
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from actstream.models import user_stream

from .serializers import ActivitySerializer


class ActivityView(ListAPIView):
    """
    List activity from various sources such as feed posts, groups and the
    marketplace.

    The response includes an `actor`, an `object` (optionally) and a `target`.

    - Actor: The object that performed the action. (normally a user)
    - Verb: The action of the activity, such as "commented".
    - Object: The object linked to the action itself.
    - Target: The object to which the activity was performed.

    So for example, "Friend (actor) commented (verb) "Great post!" (object) in
    "About the Library" (target).

    These terms are explained in greater detail
    [here](http://django-activity-stream.readthedocs.io/en/latest/concepts.html).

    - Filter by: Let me know what you want.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerializer

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    def get_queryset(self):
        return user_stream(self.request.user)
