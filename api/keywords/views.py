from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated

from .models import Keyword
from .serializers import KeywordSerializer


class KeywordViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
    GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, uni=self.request.user.uni)

    def get_serializer_context(self):
        return {'auth_user': self.request.user}
