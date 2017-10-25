from rest_framework import serializers

from users.serializers import UserSerializer
from core.serializers import CategorySerializer
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        ret['category'] = CategorySerializer(instance.category).data
        return ret

    class Meta:
        model = Item
        fields = (
            'user', 'title', 'description', 'price', 'photo', 'category',
            'status')
        read_only_fields = ('user',)
