"""Activity serializers"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from actstream.models import Action

from users.serializers import UserSerializer


class GeneralModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, instance):
        self.Meta.model = type(instance)
        super().__init__(instance=instance)


class ActivitySerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    actor_type = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()
    target_type = serializers.SerializerMethodField()
    actor = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    verb = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = (
            'id', 'created', 'title', 'actor', 'verb', 'object_type', 'object',
            'target_type', 'target')
        read_only_fields = fields

    def get_title(self, instance):
        return str(instance)

    def get_actor_type(self, obj):
        content_type, pk = (
            obj.actor_content_type, obj.actor_object_id)
        if content_type and pk:
            return str(content_type)

    def get_object_type(self, obj):
        content_type, pk = (
            obj.action_object_content_type, obj.action_object_object_id)
        if content_type and pk:
            return str(content_type)

    def get_target_type(self, obj):
        content_type, pk = (
            obj.target_content_type, obj.target_object_id)
        if content_type and pk:
            return str(content_type)

    def get_actor(self, instance):
        context = {'auth_user': self.context['auth_user']}
        user = get_user_model().objects.get(pk=instance.actor_object_id)
        return UserSerializer(user, context=context).data

    def get_object(self, obj):
        content_type, pk = (
            obj.action_object_content_type, obj.action_object_object_id)
        if content_type and pk:
            model_class = content_type.model_class()
            try:
                instance = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                return None
            return GeneralModelSerializer(instance=instance).data
        else:
            return None

    def get_target(self, obj):
        content_type, pk = obj.target_content_type, obj.target_object_id
        if content_type and pk:
            model_class = content_type.model_class()
            try:
                instance = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                return None
            return GeneralModelSerializer(instance=instance).data
        else:
            return None

    def get_timesince(self, obj):
        return obj.timesince()

    def get_verb(self, obj):
        return obj.verb
