from django.db.models import Q
from django.http import HttpResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.decorators import list_route
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .permissions import IsEnrolleeOrReadOnly
from .models import Subject, SubjectEnrollee
from .serializers import SubjectSerializer, SubjectEnrolleeSerializer
from .resources import SubjectResource


class SubjectViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    List, create and update subjects.

    - Filter by: `year`.
    - Search: `name` and `code`.
    - Order by: `created`, `modified`, `name`, `year`.
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = SubjectSerializer
    filter_fields = ('year',)
    search_fields = ('name', 'code')
    ordering_filters = ('created', 'modified', 'name', 'year')
    ordering = ('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, uni=self.request.user.uni)

    def get_queryset(self):
        return Subject.objects.filter(uni=self.request.user.uni)

    @list_route(methods=['post'])
    def upload(self, request):
        csv = request.data['file'].file.getvalue()
        resource = SubjectResource()
        result = resource.import_csv(csv, request.user.uni, request.user)
        if result.has_errors():
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=200)


class EnrolledSubjectsViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    List, enroll, or unenroll in subjects.

    - Filter by: `year`, `semester`, `subject`.
    - Order by: `year`, `semester`.
    """
    permission_classes = (IsAuthenticated, IsEnrolleeOrReadOnly)
    serializer_class = SubjectEnrolleeSerializer
    filter_fields = ('year', 'semester', 'subject')
    ordering_fields = ('created', 'modified', 'year', 'semester')
    ordering = ('-year', 'semester')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.query_params.get('user')
        if not user:
            user = self.request.user
        return SubjectEnrollee.objects.filter(user=user)
