from rest_framework import serializers

from universities.serializers import UniversitySerializer
from subjects.serializers import SubjectSerializer
from users.serializers import UserSerializer
from .models import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['uni'] = UniversitySerializer(instance.uni).data
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        ret['subject'] = SubjectSerializer(instance.subject).data
        return ret

    class Meta:
        model = Keyword
        fields = ('id', 'user', 'uni', 'subject', 'word')
        read_only_fields = ('id', 'user', 'uni')
