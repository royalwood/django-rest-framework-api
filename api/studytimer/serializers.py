from rest_framework import serializers

from .models import Entry
from subjects.serializers import SubjectSerializer


class EntrySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject'] = SubjectSerializer(instance.subject).data
        return ret

    class Meta:
        model = Entry
        fields = (
            'id', 'subject', 'start_time', 'end_time', 'date', 'total_minutes',
            'active')
        read_only_fields = ('id',)
