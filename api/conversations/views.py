from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSenderOrReceiver
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsSenderOrReceiver)
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user).order_by('-modified')
