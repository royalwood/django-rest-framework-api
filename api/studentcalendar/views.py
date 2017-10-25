from django.db.models.signals import post_save
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwner
from .serializers import CalendarSerializer
from .models import Calendar


class CalendarViewSet(UpdateModelMixin, GenericViewSet):
    """Needs some work. Will come back to it."""
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = CalendarSerializer
    filter_fields = ('title', 'type', 'subject')
    ordering = ('-modified')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)
