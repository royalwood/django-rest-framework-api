from rest_framework import serializers

from .models import Subject, SubjectEnrollee


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('user', 'campus', 'name', 'code', 'year')
        read_only_fields = ('user',)


class SubjectEnrolleeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject'] = SubjectSerializer(instance.subject).data
        return ret

    class Meta:
        model = SubjectEnrollee
        fields = ('semester', 'year', 'subject')
