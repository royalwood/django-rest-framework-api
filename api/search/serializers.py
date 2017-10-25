from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserSerializer
from groups.models import (
    Club, CustomGroup, StudentService, StudyGroup, MentorGroup)
from groups.serializers import (
    ClubSerializer, CustomGroupSerializer, StudentServiceSerializer,
    StudyGroupSerializer, MentorGroupSerializer)
from marketplace.models import Item
from subjects.models import Subject
from subjects.serializers import SubjectSerializer
from marketplace.serializers import ItemSerializer


def response(type_, label, data):
    return {'type': type_, 'label': label, 'data': data}


class SearchSerializer(serializers.Serializer): #pylint:disable=abstract-method
    def to_representation(self, obj):
        if isinstance(obj, get_user_model()):
            context = {'auth_user': self.context['auth_user']}
            serializer = UserSerializer(obj, context=context)
            return response('user', obj.name, serializer.data)
        elif isinstance(obj, Item):
            serializer = ItemSerializer(obj, context=self.context)
            return response('item', obj.title, serializer.data)
        elif isinstance(obj, Subject):
            serializer = SubjectSerializer(obj, context=self.context)
            return response('subject', obj.name, serializer.data)
        elif isinstance(obj, Club):
            serializer = ClubSerializer(obj, context=self.context)
            return response('club', obj.name, serializer.data)
        elif isinstance(obj, CustomGroup):
            serializer = CustomGroupSerializer(obj, context=self.context)
            return response('customgroup', obj.name, serializer.data)
        elif isinstance(obj, StudentService):
            serializer = StudentServiceSerializer(obj, context=self.context)
            return response('studentservice', obj.name, serializer.data)
        elif isinstance(obj, StudyGroup):
            serializer = StudyGroupSerializer(obj, context=self.context)
            return response('studygroup', obj.name, serializer.data)
        elif isinstance(obj, MentorGroup):
            serializer = MentorGroupSerializer(obj, context=self.context)
            return response('mentorgroup', obj.name, serializer.data)
        else:
            raise Exception('Instance does not exist')
