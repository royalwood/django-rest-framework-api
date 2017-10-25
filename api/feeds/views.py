import json

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route

from karma.models import History
from .permissions import IsPosterOrReadOnly, IsAnswerer
from .models import Post, Comment, PollAnswer, PostLog
from .serializers import (
    PostSerializer, PollAnswerSerializer, PostLogSerializer, CommentSerializer)


class PostViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    GenericViewSet):
    """
    List, retrieve, create and update posts.

    - Filter by: `feed_object`, `feed_object_id`, `campus`, `school`, and
      `course`.
    - Search: `title` and `body`.
    - Order by: `created`, `modified`, `title`.
    """
    permission_classes = (IsAuthenticated, IsPosterOrReadOnly)
    serializer_class = PostSerializer
    filter_fields = ('feed_object', 'feed_object_id', 'campus', 'school', 'course')
    search_fields = ('title', 'body')
    ordering_filters = ('created', 'modified', 'title')
    ordering = ('-pinning_date', '-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, uni=self.request.user.uni)

    def get_serializer_context(self):
        return {'auth_user': self.request.user}

    def get_queryset(self):
        # Query
        queryset = Post.objects
        queryset = queryset.filter(uni=self.request.user.uni)
        # Remove any unscheduled
        datetime_now = timezone.now()
        queryset = queryset.filter(
            Q(scheduled_start_date__lte=datetime_now, scheduled_end_date__gte=datetime_now) | Q(scheduled_start_date=None) | Q(scheduled_end_date=None))

        # Targeting posts
        # Targeting field must be a JSON object like {"faculty":[1,2,3],
        # "campus":[1,5,6], "year_level": "first", "international": false} Or it
        # should be saved blank

#        if all_students == 'True' or all_students == 'true':
#            final_post_list = []
#            user = self.request.user
#            my_faculty = user.school
#            my_campus = user.campus
#            my_year_of_completion = user.year_of_completion
#            my_year_of_start = user.start_year
#            i_am_international = False
#
#            if user.international:
#                i_am_international = True
#
#            for post in queryset:
#                if post.targeting:
#                    target_obj = json.loads(post.targeting)
#                    faculty_check = False
#                    campus_check = False
#                    year_level_check = False
#                    international_check = False
#
#                    if target_obj["faculty"] and my_faculty.id in target_obj["faculty"]:
#                        faculty_check = True
#
#                    if target_obj["international"] is not None:
#                        if target_obj["international"] == i_am_international:
#                            international_check = True
#
#                    if target_obj["campus"] and my_campus.id in target_obj["campus"]:
#                        campus_check = True
#
#                    if target_obj["year_level"]:
#                        if target_obj["year_level"] == 'first':
#                            if (timezone.now().year - my_year_of_start) <= 1 and (timezone.now().year - my_year_of_start) >= 0:
#                                year_level_check = True
#                        elif target_obj["year_level"] == 'final':
#                            if timezone.now().year == my_year_of_completion:
#                                year_level_check = True
#
#                    if faculty_check and international_check and campus_check and year_level_check:
#                        final_post_list.append(post.id)
#
#            queryset = queryset.filter(id__in=final_post_list)

        return queryset

    def destroy(self, request, *args, **kwargs):
        """Delete a post - need to add a log entry."""
        post = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        if (response.status_code == status.HTTP_204_NO_CONTENT):
            PostLog.objects.create(
                post=post, user=request.user, status=PostLog.STATUS.removed)
        return response

    @detail_route(methods=['POST'])
    def report(self, request):
        user = self.request.query_params.get('user')
        if not user:
            msg = 'You must specify the post'
            raise ValidationError(msg)
        comment = self.request.query_params.get('comment', '')
        post = self.get_object()
        post.report(request.user, comment)

    @detail_route(methods=['POST'])
    def clear(self, request):
        user = self.request.query_params.get('user')
        if not user:
            msg = 'You must specify the post'
            raise ValidationError(msg)
        comment = self.request.query_params.get('comment', '')
        post = self.get_object()
        post.clear(request.user, comment)


class CommentViewSet(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """List, create, update comments for a post

    - Filter by: `post` (required).
    - Search: `text`.
    - Order by: `created`, `modified`.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(status=True)
    filter_fields = ('post',)
    search_fields = ('text',)
    ordering_filters = ('created', 'modified')
    ordering = ('created',)

    def get_queryset(self):
        if not 'post' in self.request.query_params:
            msg = 'You must specify the post'
            raise ValidationError(msg)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLogViewSet(ListModelMixin, GenericViewSet):
    """List moderation log entries for a post.

    - Filter by: `post` (required).
    - Search: `text`.
    - Order by: `created`, `modified`.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLogSerializer
    queryset = PostLog.objects.all()
    filter_fields = ('post',)

    def get_queryset(self):
        if not 'post' in self.request.query_params:
            msg = 'You must specify the post'
            raise ValidationError(msg)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PollAnswerViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsAnswerer)
    queryset = PollAnswer.objects.all()
    serializer_class = PollAnswerSerializer

    def get_queryset(self):
        if not 'post' in self.request.query_params:
            msg = 'You must specify the post'
            raise ValidationError(msg)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
