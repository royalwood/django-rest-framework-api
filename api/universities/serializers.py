from rest_framework import serializers

from .models import University, Campus, School, Course


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('name', 'address')


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('name',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'code',)


class UniversitySerializer(serializers.ModelSerializer):
    campuses = CampusSerializer(many=True, read_only=True)
    schools = SchoolSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = (
            'id', 'name', 'code', 'state', 'aaf', 'campuses', 'schools')
        read_only_fields = ('id',)
