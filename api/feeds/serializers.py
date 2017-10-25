from rest_framework import serializers

from users.serializers import UserSerializer
from universities.serializers import (
    CampusSerializer, SchoolSerializer, CourseSerializer)
from .models import Post, PollAnswer, PostLog, Comment


class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        return ret

    class Meta:
        model = Comment
        fields = (
            'id', 'created', 'user', 'text', 'status', 'is_anonymous')
        read_only_fields = ('id', 'created', 'user', 'status', 'is_anonymous')


class FullCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        ret['post'] = PostSerializer(instance.post, context=context).data
        return ret

    class Meta:
        model = Comment
        fields = (
            'id', 'created', 'user', 'post', 'text', 'status', 'is_anonymous')
        read_only_fields = ('id', 'created', 'user', 'status', 'is_anonymous')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source='first_comments')
    campus = CampusSerializer()
    school = SchoolSerializer()
    course = CourseSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        # Some clients want markdown, others want html
        fmt = self.context.get('fmt')
        if fmt == 'plain':
            ret['body'] = instance.body_plain
        elif fmt == 'markdown':
            ret['body'] = instance.body_markdown
        elif fmt == 'html':
            ret['body'] = instance.body_html
        else:
            ret['body'] = instance.body_html
        return ret

    class Meta:
        model = Post
        fields = (
            'id', 'created', 'user', 'uni', 'feed_object', 'feed_object_id',
            'campus', 'school', 'course', 'title', 'body', 'status',
            'status_changed', 'is_international', 'is_anonymous', 'likes_count',
            'tags', 'type', 'total_comments', 'targeting', 'comments')
        read_only_fields = (
            'id', 'created', 'user', 'uni', 'total_comments', 'comments')

    def validate(self, data):
        try:
            Group.objects.get_group_from_feed_object(
                data['feed_object'], data['feed_object_id'])
        except ObjectDoesNotExist:
            raise ValidationError('Posting into group that doesn\'t exist')


class PollAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAnswer
        fields = ('post', 'answer')


class PostLogSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = UserSerializer(
            instance.user, context={'auth_user': self.context['auth_user']}).data
        ret['post'] = PostSerializer(instance.post).data
        return ret

    class Meta:
        model = PostLog
        fields = ('created', 'user', 'post', 'status', 'comment')
        read_only_fields = ('created', 'user', 'status')
