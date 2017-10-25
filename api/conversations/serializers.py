from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['sender'] = UserSerializer(
            instance.sender, context={'auth_user': self.context['auth_user']}).data
        return ret

    class Meta:
        model = Message
        fields = (
            'created', 'modified', 'sender', 'text', 'is_attachments',
            'is_read')
        read_only_fields = ('created', 'modified', 'sender')
