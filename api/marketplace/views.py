from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSellerOrReadOnly
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    GenericViewSet):
    """
    List, retrieve, create, or update marketplace items.

    - Filter by: `user`, `category`.
    - Search: `name`, `description`.
    - Order by: `created`, `modified`, `name`.
    """
    permission_classes = (IsAuthenticated, IsSellerOrReadOnly)
    serializer_class = ItemSerializer
    search_fields = ('name', 'description')
    filter_fields = ('user', 'category')
    ordering_fields = ('created', 'modified', 'name')
    ordering = ('-created',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    def get_queryset(self):
        return Item.objects.filter(status=True)
