from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwner
from .models import Entry
from .serializers import EntrySerializer


class EntryViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """Needs work. Will come back to it."""
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = EntrySerializer
    filter_fields = ('subject', 'active')
    ordering = ('-active', 'start_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Entry.objects.filter(user=self.request.user)
