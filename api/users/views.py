import random
import string
from itertools import chain

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from subjects.models import SubjectEnrollee
from groups.models import (
    CustomGroupMember, StudyGroupMember, ClubMember, StudentServiceMember)
from .models import (
    User, BlockedUser, UserProfileDetail, Connection, VerificationCode)
from .serializers import (
    UserSerializer, FullUserSerializer, BlockedUserSerializer,
    UserProfileDetailSerializer)
from .signals import request_demo
from .serializers import ResetPasswordSerializer


class UserViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    GenericViewSet):
    """
    List, retrieve, create and update users.

    - Search: `name`.
    - Order by: `created`, `modified`, `name`.

    To connect to a user, send either a get or post request to
    `users/1/connect`, with no data. To disconnect, send to
    `users/1/disconnect`. To block, send to `users/1/block`. To unblock, send
    the disconnect one.
    """
    # Authenticated users need to list other users (such as when finding someone
    # to connect to). Only admin can modify users.
    permission_classes = (AllowAny,)
#    permission_classes = (DjangoModelPermissions,)
    serializer_class = FullUserSerializer
    search_fields = ('name')
    ordering_fields = ('created', 'modified', 'name')
    ordering = ('name',)

    def perform_create(self, serializer):
        serializer.save(uni=self.request.user.uni)

    def get_queryset(self):
        return User.objects.filter(uni=self.request.user.uni, is_active=True)

#        if on_campus:
#            users_campus = user.campus
#            users_campus_longitude = user.campus.longitude
#            users_campus_latitude = user.campus.latitude
#
#            lat = float(users_campus_latitude)
#            lon = float(users_campus_longitude)
#
#            earth_radius = 6378.1  # earth radius
#            distance = 2  # distance in km
#
#            lat1 = lat - math.degrees(distance / earth_radius)
#            lat2 = lat + math.degrees(distance / earth_radius)
#            long1 = lon - math.degrees(distance / earth_radius / math.cos(math.degrees(lat)))
#            long2 = lon + math.degrees(distance / earth_radius / math.cos(math.degrees(lat)))
#
#            queryset = queryset.filter(campus=users_campus).filter(on_campus=True)\
#                .filter(latitude__gte=lat1, latitude__lte=lat2)\
#                .filter(longitude__gte=long1, longitude__lte=long2)

    @list_route(methods=['post'])
    def makeadmin(self, request):
        """Makes a user an admin of the uni (gives them admin priveleges)"""
        email = request.data.get('email')
        if not email:
            raise ValidationError('Email is required')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound('User not found')
        group = Group.objects.get(name='Uni Admin')
        user.groups.add(group)
        return Response(None, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def removeadmin(self, request):
        """Makes a user an admin of the uni (gives them admin priveleges)"""
        email = request.data.get('email')
        if not email:
            raise ValidationError('Email is required')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound('User not found')
        group = Group.objects.get(name='Uni Admin')
        user.groups.remove(group)
        return Response(None, status=status.HTTP_200_OK)

    @detail_route(methods=['get', 'post'])
    def connect(self, request, pk):
        """Connects the auth user to the specified user"""
        user = self.get_object()
        self.request.user.add_connection(user)
        return Response(None, status=status.HTTP_200_OK)

    @detail_route(methods=['get', 'post'])
    def disconnect(self, request, pk):
        """Disconnects the auth user from the specified user"""
        user = self.get_object()
        self.request.user.remove_connection(user)
        return Response(None, status=status.HTTP_200_OK)

    @detail_route(methods=['get', 'post'])
    def block(self, request, pk):
        """Blocks the specified user from the auth user. To unblock, call
        disconnect
        """
        user = self.get_object()
        self.request.user.block_connection(user)
        return Response(None, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def demo(self, request):
        name = request.data.get("name")
        institute = request.data.get("institute")
        role = request.data.get("role")
        email = request.data.get('email')
        phone = request.data.get("phone")
        request_demo(name, institute, role, email, phone)
        return Response("OK", status=status.HTTP_200_OK)


class MeViewSet(GenericViewSet):
    """Retrieve the currently authenticated user, including their permissions
    (eventually), and allows you to update their profile."""
    # These views only work on the authenticated user's record. So the only
    # requirement is that the user is logged in.
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            raise NotFound('User {} not found'.format(request.user.id))
        serializer = FullUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            raise NotFound('User {} not found'.format(request.user.id))
        serializer = FullUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            raise NotFound('User {} not found'.format(request.user.id))
        serializer = FullUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserProfileDetailSerializer
    queryset = UserProfileDetail.objects.all()
    filter_fields = ('user',)


class ConnectionViewSet(ListModelMixin, GenericViewSet):
    """
    Retrieves the connections of the authenticated user, or a specified user.

    - Filter by: `user`, `status`

    Valid options when filtering by `status` are:

    - `pending`: awaiting the user's acceptance.
    - `requested`: awaiting another user's acceptance.
    - `accepted`: both users have accepted the connection.
    - `blocked`: users the user has blocked.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    def get_queryset(self):
        # Get specified user object
        user = self.request.query_params.get('user')
        if user:
            try:
                user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                raise NotFound('User {} not found'.format(request.user.id))
        # Otherwise use the auth user
        else:
            user = self.request.user
        # Return different queryset depending on the status
        status = self.request.query_params.get('status')
        if status == Connection.STATUS.pending:
            return user.get_pending_connections()
        if status == 'requested': # This is not a status that's stored
            return user.get_requested_connections()
        elif status == Connection.STATUS.accepted:
            return user.get_accepted_connections()
        elif status == Connection.STATUS.blocked:
            return user.get_blocked_connections()
        return user.get_connections()


class ResetPasswordViewSet(views.APIView):
    # Anyone can reset their password
    permission_classes = (AllowAny,)

    def get(self, request, format=None): #pylint:disable=redefined-builtin,unused-argument

        token = self.request.query_params.get('token')

        obj = {}

        if token is not None and token == "05069046-1821-4dee-8f86-453e6f4203fa":
            step = self.request.query_params.get('step')

            obj['status'] = False

            if step == "1":
                email = self.request.query_params.get('email')

                if email is not None:
                    queryset = User.objects.all().filter(email=email)[:1]

                    # Email Verified!
                    if queryset.exists():
                        obj['status'] = True

                        # generating verification random code
                        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

                        rpObj = {}
                        rpObj['email'] = email
                        rpObj['code'] = code

                        # Sending verification code by email
                        EmailMsg = EmailMessage('UCROO - Password Reset - Verification Code',
                                                '<strong>Please use this code to create a new password.</strong>'
                                                '<br><br> Your verification code is: <br><h3>%s</h3>' % code,
                                                'no-reply@sucroo.com', ['%s' % email])
                        EmailMsg.content_subtype = "html"
                        EmailMsg.send()

                        VerificationCode.objects.all().filter(email=email).delete()

                        serializer = ResetPasswordSerializer(data=rpObj)
                        serializer.is_valid()
                        serializer.save()

            elif step == "2":
                code = self.request.query_params.get('code')
                email = self.request.query_params.get('email')

                if code is not None and email is not None:
                    queryset = User.objects.all().filter(email=email)[:1]
                    if queryset.exists():
                        token_queryset = VerificationCode.objects.all().filter(email=email).filter(code=code)[:1]
                        if token_queryset.exists():
                            obj['status'] = True

            elif step == "3":
                code = self.request.query_params.get('code')
                email = self.request.query_params.get('email')

                if code is not None and email is not None:
                    queryset = User.objects.all().filter(email=email)[:1]

                    if queryset.exists():
                        token_queryset = VerificationCode.objects.all().filter(email=email).filter(code=code)[:1]
                        if token_queryset.exists():
                            pw = self.request.query_params.get('pass')
                            if pw is not None:
                                obj['status'] = True

                                # Encrypting password
                                password = make_password(password=pw, salt=None, hasher='default')

                                # Updating password
                                User.objects.all().filter(email=email).update(password=password)

                                # deleting verification code
                                VerificationCode.objects.all().filter(email=email).delete()

        return Response(obj)


#class SuggestedViewSet(ListModelMixin, GenericViewSet):
#    # Anyone can reset their password
#    permission_classes = (AllowAny,)
#    serializer_class = UserSerializer
#
#    def get_queryset(self):
#        user = self.request.user
#        limit = int(self.request.query_params.get('limit', 0))
#
#        # Connection to a connection of a user
#        i_added_users = list(set(Connection.objects.all().filter(user_1=user).values_list('user_2', flat=True)))
#        users_added_me = list(set(Connection.objects.all().filter(user_2=user).values_list('user_1', flat=True)))
#        my_connection_list = i_added_users + users_added_me
#
#        queryset = User.objects.all().exclude(id=user.id).exclude(id__in=my_connection_list)
#
#        connections_of_my_connections_user1 = list(set(Connection.objects.filter(user_2__in=my_connection_list).exclude(user_1__in=my_connection_list).exclude(user_1=user).values_list('user_1', flat=True)))
#        connections_of_my_connections_user2 = list(set(Connection.objects.filter(user_1__in=my_connection_list).exclude(user_2__in=my_connection_list).exclude(user_2=user).values_list('user_2', flat=True)))
#        suggested_connections = connections_of_my_connections_user1 + connections_of_my_connections_user2
#
#        querysetA = queryset.filter(id__in=suggested_connections)
#
#        # Users from Groups (i.e. Custom Groups, Study Groups, Club Pages, Student Service Pages)
#        my_custom_groups = list(set(CustomGroupMember.objects.all().filter(user=user).values_list('customgroups', flat=True)))
#        users_in_same_custom_group = list(set(CustomGroupMember.objects.all().filter(user__in=my_custom_groups).exclude(user=user).values_list('user', flat=True)))
#
#        my_study_groups = list(set(StudyGroupMember.objects.all().filter(user=user).values_list('study_group', flat=True)))
#        users_in_same_study_group = list(set(StudyGroupMember.objects.all().filter(user__in=my_study_groups).exclude(user=user).values_list('user', flat=True)))
#
#        my_club_groups = list(set(ClubMember.objects.all().filter(user=user).values_list('club', flat=True)))
#        users_in_same_club_group = list(set(ClubMember.objects.all().filter(user__in=my_club_groups).exclude(user=user).values_list('user', flat=True)))
#
#        my_student_services_groups = list(set(StudentServiceMember.objects.all().filter(user=user).values_list('student_service', flat=True)))
#        users_in_same_student_services_group = list(set(StudentServiceMember.objects.all().filter(user__in=my_student_services_groups).exclude(user=user).values_list('user', flat=True)))
#
#        all_users_in_groups_list = users_in_same_custom_group + users_in_same_study_group + users_in_same_club_group + users_in_same_student_services_group
#
#        querysetB = queryset.filter(id__in=all_users_in_groups_list).exclude(id__in=suggested_connections)
#
#        # Same subject
#        my_subjects_list = list(set(SubjectEnrollee.objects.all().filter(user=user).values_list('subject', flat=True)))
#        user_having_same_subjects = list(set(SubjectEnrollee.objects.all().filter(subject__in=my_subjects_list).exclude(user=user).values_list('user', flat=True)))
#
#        querysetC = queryset.filter(id__in=user_having_same_subjects).exclude(id__in=suggested_connections).exclude(id__in=all_users_in_groups_list)
#
#        # Same campus
#        users_in_same_campus = list(set(User.objects.all().filter(campus=user.campus).exclude(id=user.id).values_list('id', flat=True)))
#
#        querysetD = queryset.filter(id__in=users_in_same_campus).exclude(id__in=suggested_connections).exclude(id__in=all_users_in_groups_list).exclude(id__in=user_having_same_subjects)
#
#        queryset = list(chain(querysetA, querysetB, querysetC, querysetD))
#
#        # queryset = queryset.exclude(id__in=my_connection_list)
#
#        if limit > 0:
#            queryset = queryset[:limit]
#
#
#        return queryset
