from itertools import chain

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

from groups.models import (
    StudyGroup, StudentService, Club, MentorGroup, CustomGroup)
from marketplace.models import Item
from subjects.models import Subject
from .serializers import SearchSerializer


class SearchView(ListAPIView):
    """
    Searches users, groups, subjects and marketplace, and returns any results in
    a generic format.

    - Filter by: `search` (required)
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SearchSerializer

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    def get_queryset(self):
        query = self.request.query_params.get('q')
        # Validate
        if not query:
            raise ValidationError('No query specified')
        # Query
        users = get_user_model().objects.search(query)
        items = Item.objects.search(query)
        subjects = Subject.objects.search(query)
        clubs = Club.objects.search(query)
        customgroups = CustomGroup.objects.search(query)
        studentservices = StudentService.objects.search(query)
        studygroups = StudyGroup.objects.search(query)
        mentorgroups = MentorGroup.objects.search(query)
        ret = list(chain(
            users, items, subjects, clubs, customgroups, studentservices,
            studygroups, mentorgroups))
        return ret
