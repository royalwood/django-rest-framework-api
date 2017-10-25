import datetime
from abc import ABCMeta, abstractmethod

from django.db.models.signals import post_save
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from actstream.actions import follow, unfollow

from .permissions import (
    IsGroupAdminOrReadOnly, IsEventOwnerOrReadOnly,
    IsEventOwnerOrAttendeeOrReadOnly)
from .models import (
    StudyGroup, StudyGroupMember, StudentService, StudentServiceAdmin,
    StudentServiceDropin, StudentServiceEvent, StudentServiceEventMember,
    StudentServiceMember, Club, MentorGroup, MentorGroupMember, CustomGroup,
    CustomGroupMember, Event, EventMember, ClubMember)
from .serializers import (
    ClubSerializer, ClubMemberSerializer, StudyGroupSerializer,
    StudyGroupMemberSerializer, StudentServiceSerializer,
    StudentServiceEventSerializer, StudentServiceEventMemberSerializer,
    StudentServiceMemberSerializer, MentorGroupSerializer,
    MentorGroupMemberSerializer, CustomGroupSerializer, JoinedGroupsSerializer,
    CustomGroupMemberSerializer, EventSerializer, EventMemberSerializer)


class GroupViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    GenericViewSet):
    """Abstract base class for all groups"""
    __metaclass__ = ABCMeta
    permission_classes = (IsAuthenticated, IsGroupAdminOrReadOnly)
    filter_fields = ('user', 'uni', 'campus', 'school')
    search_fields = ('name',)
    ordering_filters = ('created', 'modified', 'name')
    ordering = ('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, uni=self.request.user.uni)

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None): #pylint:disable=unused-argument
        group = self.get_object()
        follow(request.user, group, actor_only=False)
        return Response(None, status=status.HTTP_200_OK)

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None): #pylint:disable=unused-argument
        group = self.get_object()
        unfollow(request.user, group)
        return Response(None, status=status.HTTP_200_OK)

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None): #pylint:disable=unused-argument
        """Leave the group"""
        group = self.get_object()
        group.remove_member(request.user)
        return Response(None, status=status.HTTP_200_OK)


class ClubViewSet(GroupViewSet):
    """
    List, retrieve, create and update Clubs.

    - Filter by: `user`, `uni`, `campus`, `school`, `category`.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    serializer_class = ClubSerializer

    def get_queryset(self):
        return Club.objects.filter(uni=self.request.user.uni)


class CustomGroupViewSet(GroupViewSet):
    """
    List, retrieve, create and update Custom Groups.

    - Filter by: `user`, `uni`, `campus`, `school`, `category`.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    serializer_class = CustomGroupSerializer
    filter_fields = GroupViewSet.filter_fields + ('category',)

    def get_queryset(self):
        return CustomGroup.objects.filter(
            private=False, uni=self.request.user.uni)
        # Trending
#        if trending == 'True':
#            queryset = queryset.order_by('-created', 'customgroupmember')[:2]
#        # Suggested
#        if suggested == "true" or suggested == "True" :
#            user = self.request.user
#            # Can be User1 or User2
#            my_connections_list = list(set(Connection.objects.all().filter(Q(user_1=user.id)).filter(accepted=True).filter(blocked=False).values_list('user_2', flat=True)))
#            my_connections_joined_groups_list = list(set(CustomGroupMember.objects.all().filter(user__in=my_connections_list).values_list('group', flat=True)))
#            my_joined_groups_list = list(set(CustomGroupMember.objects.all().filter(user=user.id).values_list('group', flat=True)))
#
#            queryset = queryset.filter(id__in=my_connections_joined_groups_list)
#            queryset = queryset.exclude(id__in=my_joined_groups_list)
#        return queryset


class StudentServiceViewSet(GroupViewSet):
    """
    List, retrieve, create and update Student Services.

    - Filter by: `user`, `uni`, `campus`, `school`.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    serializer_class = StudentServiceSerializer

    def get_queryset(self):
        return StudentService.objects.filter(
            private=False, uni=self.request.user.uni)


class StudyGroupViewSet(GroupViewSet):
    """
    List, retrieve, create and update Study Groups.

    - Filter by: `user`, `uni`, `campus`, `school`.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    serializer_class = StudyGroupSerializer

    def get_queryset(self):
        return StudyGroup.objects.filter(
            private=False, uni=self.request.user.uni)


class MentorGroupViewSet(GroupViewSet):
    """
    List, retrieve, create and update Mentor Groups.

    - Filter by: `user`, `uni`, `campus`, `school`.
    - Search: `name`.
    - Order by: `created`, `modified`, `name`.
    """
    serializer_class = MentorGroupSerializer

    def get_queryset(self):
        return MentorGroup.objects.filter(uni=self.request.user.uni)


class GroupMemberViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    filter_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'auth_user': self.request.user}


class ClubMemberViewSet(GroupMemberViewSet):
    permission_classes = (IsAuthenticated,) # For now
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = ClubMemberSerializer
    queryset = ClubMember.objects.all()


class CustomGroupMemberViewSet(GroupMemberViewSet):
    permission_classes = (IsAuthenticated,) # For now
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = CustomGroupMemberSerializer
    queryset = CustomGroupMember.objects.all()


class StudentServiceMemberViewSet(GroupMemberViewSet):
    permission_classes = (IsAuthenticated,)
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = StudentServiceMemberSerializer
    queryset = StudentServiceMember.objects.all()


class StudyGroupMemberViewSet(GroupMemberViewSet):
    permission_classes = (IsAuthenticated,) # For now
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = StudyGroupMemberSerializer
    queryset = StudyGroupMember.objects.all()


class MentorGroupMemberViewSet(GroupMemberViewSet):
    permission_classes = (IsAuthenticated,) # For now
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = MentorGroupMemberSerializer
    queryset = MentorGroupMember.objects.all()


class StudentServiceAdminViewSet(
    ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentServiceSerializer
    queryset = StudentServiceAdmin.objects.all()
    filter_fields = ('group',)


class StudentServiceDropinViewSet(
    ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentServiceSerializer
    filter_fields = ('group',)

    def get_queryset(self):
        queryset = StudentServiceDropin.objects.filter(
            campus=self.request.user.campus)


class StudentServiceEventViewSet(
    ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,) # For now
    serializer_class = StudentServiceEventSerializer
    filter_fields = ('group', 'campus')
    search_fields = ('name', 'description')

    def get_queryset(self):
        return StudentServiceEvent.objects.filter(
            campus=self.request.user.campus)


class StudentServiceEventMemberViewSet(
    ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,) # For now
#    permission_classes = (IsAuthenticated, IsMemberOrIsGroupAdminOrReadOnly)
    serializer_class = StudentServiceEventMemberSerializer
    queryset = StudentServiceEventMember.objects.all()
    filter_fields = ('event',)


class EventViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """Authenticated users can see any event, owners can modify their own
    event.
    """
    permission_classes = (IsAuthenticated, IsEventOwnerOrReadOnly)
    serializer_class = EventSerializer
    filter_fields = ('module', 'module_name', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    ordering = ('-modified',)

    def get_queryset(self):
        queryset = Event.objects.filter(uni=self.request.user.uni)


class EventMemberViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """Attendees can modify their own attendance, event owners can modify any,
    other authenticated users can view.
    """
    permission_classes = (IsAuthenticated, IsEventOwnerOrAttendeeOrReadOnly)
    serializer_class = EventMemberSerializer
    queryset = EventMember.objects.all()
    filter_fields = ('event',)


class JoinedGroupsView(ListAPIView):
    """
    List all joined groups, 3 per type.

    Filter by: `user`. (If not specified, returns the auth user's groups.)
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinedGroupsSerializer

    def list(self, request):
        user = self.request.query_params.get('user', None)
        # Get specified user, otherwise auth user
        if not user:
            user = self.request.user
        # Query
        club = ClubMember.objects.filter(user=user)[:3]
        club = [member.group for member in club]
        customgroup = CustomGroupMember.objects.filter(user=user)[:3]
        customgroup = [member.group for member in customgroup]
        studentservice = StudentServiceMember.objects.filter(user=user)[:3]
        studentservice = [member.group for member in studentservice]
        studygroup = StudyGroupMember.objects.filter(user=user)[:3]
        studygroup = [member.group for member in studygroup]
        mentorgroup = MentorGroupMember.objects.filter(user=user)[:3]
        mentorgroup = [member.group for member in mentorgroup]
        # Serialize and return
        context = {'auth_user': self.request.user}
        ret = {
            'clubs': ClubSerializer(club, many=True, context=context).data,
            'customgroups': CustomGroupSerializer(customgroup, many=True,
                context=context).data,
            'studentservices': StudentServiceSerializer(
                studentservice, many=True, context=context).data,
            'studygroups': StudyGroupSerializer(studygroup, many=True,
                context=context).data,
            'mentorgroups': MentorGroupSerializer(mentorgroup, many=True,
                context=context).data,
        }
        return Response(ret, status=status.HTTP_200_OK)
