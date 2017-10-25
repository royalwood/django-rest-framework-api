from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly)
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.decorators import list_route
from rest_framework.parsers import MultiPartParser

from .models import University, Campus, School, Course
from .serializers import (
    UniversitySerializer, CampusSerializer, SchoolSerializer, CourseSerializer)
from .resources import CampusResource, SchoolResource, CourseResource


class UniversityViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    List and update universities.

    - Filter by: `sign_up` (restricts results to unis that can be signed up to).
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    # Unauthenticated users do need to list unis when logging in or signing up.
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    search_fields = ('name',)
    filter_fields = ('sign_up',)
    ordering_fields = ('created', 'modified', 'name')
    ordering = ('name',)


class CampusViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    List, create and update campuses.

    - Filter by: `uni`. Required for unauthenticated users, ignored for
      authenticated users.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    # Unauthenticated users need the list of campuses when logging in or signing
    # up.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser,)
    serializer_class = CampusSerializer
    filter_fields = ('uni',)
    search_fields = ('name',)
    ordering_fields = ('created', 'modified', 'name')
    ordering = ('name',)

    def perform_create(self, serializer):
        serializer.save(uni=self.request.user.uni)

    def get_queryset(self):
        queryset = Campus.objects.all()
        # Authenticated users, show only courses for their uni
        if self.request.user.is_authenticated():
            queryset = queryset.filter(uni=self.request.user.uni)
        # Unauthenticated must filter by uni
        else:
            if not 'uni' in self.request.query_params:
                raise ValidationError('Anonymous users must specify the uni')
        return queryset

    @list_route(methods=['post'])
    def upload(self, request):
        csv = request.data['file'].file.getvalue()
        resource = CampusResource()
        result = resource.import_csv(csv, request.user.uni)
        if result.has_errors():
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=200)


class SchoolViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """List, create and update schools.

    - Filter by: `uni`. Required for unauthenticated users, ignored for
      authenticated users.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    # Unauthenticated users need the list of schools when logging in or
    # signing up.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SchoolSerializer
    filter_fields = ('uni',)
    search_fields = ('name',)
    ordering_fields = ('created', 'modified', 'name',)
    ordering = ('name',)

    def perform_create(self, serializer):
        serializer.save(uni=self.request.user.uni)

    def get_queryset(self):
        queryset = School.objects.all()
        # Authenticated users, show only courses for their uni
        if self.request.user.is_authenticated():
            queryset = queryset.filter(uni=self.request.user.uni)
        # Unauthenticated must filter by uni
        else:
            if not 'uni' in self.request.query_params:
                raise ValidationError('Anonymous users must specify the uni')
        return queryset

    @list_route(methods=['post'])
    def upload(self, request):
        csv = request.data['file'].file.getvalue()
        resource = SchoolResource()
        result = resource.import_csv(csv, request.user.uni)
        if result.has_errors():
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=200)


class CourseViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    List, create, update, and import courses.

    - Filter by: `uni`. Required for unauthenticated users, ignored for
      authenticated users.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    # Any authenticated user can see courses (of the user's own uni), but
    # requires model permissions to add/change/delete.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CourseSerializer
    filter_fields = ('uni',)
    search_fields = ('name',)
    ordering_fields = ('created', 'modified', 'name')
    ordering = ('name',)

    def perform_create(self, serializer):
        serializer.save(uni=self.request.user.uni)

    def get_queryset(self):
        queryset = Course.objects.all()
        # Authenticated users, show only courses for their uni
        if self.request.user.is_authenticated():
            queryset = queryset.filter(uni=self.request.user.uni)
        # Unauthenticated must filter by uni
        else:
            if not 'uni' in self.request.query_params:
                raise ValidationError('Anonymous users must specify the uni')
        return queryset

    @list_route(methods=['post'])
    def upload(self, request):
        csv = request.data['file'].file.getvalue()
        resource = CourseResource()
        result = resource.import_csv(csv, request.user.uni)
        if result.has_errors():
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=200)
