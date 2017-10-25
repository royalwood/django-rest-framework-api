from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .serializers import AppVersionSerializer, CategorySerializer
from .models import AppVersion, Category


class AppVersionViewSet(ListModelMixin, GenericViewSet):
    # Unauthenticated users can see the response from this.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AppVersionSerializer

    def get_queryset(self):
        return AppVersion.objects.all().order_by('-id')[:1]


class CategoryViewSet(ListModelMixin, GenericViewSet):
    """These categories seem to be used for marketplace and customgroup
    categories, but we might be better to have separate tables like
    marketplace_type and groups_type
    """
    # Any authenticated user can see categories, but only admins can edit them.
    permission_classes = (IsAdminUser,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().order_by('-id')[:1]
