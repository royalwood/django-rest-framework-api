from rest_framework import serializers

from subjects.serializers import SubjectSerializer
from .models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject'] = SubjectSerializer(instance.subject).data
        return ret

    class Meta:
        model = Calendar
        fields = (
            'subject', 'type', 'class_type', 'title', 'location',
            'description', 'time_from', 'time_to', 'time_day',
            'is_all_day_event', 'color', 'by_academic', 'recurring_rule',
            'assessment_date', 'assessment_time', 'assessment_alert',
            'event_cal_type')
