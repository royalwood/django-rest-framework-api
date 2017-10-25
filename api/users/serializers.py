from django.contrib.auth.models import Permission
from rest_framework import serializers

from universities.serializers import (
    UniversitySerializer, CampusSerializer, CourseSerializer)
from .models import User, Group, BlockedUser, UserProfileDetail, VerificationCode


#class PermissionSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Permission
#        depth = 1
#        fields = ('user',)


#class GroupSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Group
#        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    """Regular user serializer. Used in most cases, unless the whole user is
    required.
    """
    campus_name = serializers.StringRelatedField(source='campus')
    school_name = serializers.StringRelatedField(source='school')
    course_name = serializers.StringRelatedField(source='course')
    is_connected = serializers.SerializerMethodField()
    connection_status = serializers.SerializerMethodField()

    def get_is_connected(self, instance):
        return self.context['auth_user'].is_connected(instance)

    def get_connection_status(self, instance):
        return self.context['auth_user'].get_connection_status(instance)

    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'gender', 'profile_pic', 'campus_name',
            'school_name', 'course_name', 'is_connected', 'connection_status')
        read_only_fields = ('id',)


class FullUserSerializer(serializers.ModelSerializer):
    """For use in user-detail routes, and the get_token route"""
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, instance):
        return instance.get_all_permissions()

    menu = serializers.SerializerMethodField()
    def get_menu(self, instance): #pylint:disable=unused-argument
        return [
            {"location": "club", "title": "Clubs & Societies"},
            {"location": "unit", "title": "Subjects"},
            {"location": "study_group", "title": "Study"},
            {"location": "student_service", "title": "Student Services"},
            {"location": "mentors", "title": "Mentors"},
            {"location": "customgroups", "title": "Custom"}
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['uni'] = UniversitySerializer(instance.uni).data
        ret['campus'] = CampusSerializer(instance.campus).data
        ret['course'] = CourseSerializer(instance.course).data
        ret['groups'] = [g.name for g in instance.groups.all()]
        return ret

    class Meta:
        model = User
        fields = (
            'android_gcm', 'android_version', 'attempt_fail', 'banner_pic',
            'campus', 'completed', 'course', 'csu_id', 'email',
            'email_notifications', 'email_secondary', 'finished', 'first_name',
            'gender', 'groups', 'hide_connection_info_popup', 'id',
            'international', 'ios_apn_token', 'iphone_version', 'is_signed_flg',
            'is_vet', 'last_name', 'latitude', 'longitude', 'menu', 'on_campus',
            'password', 'permissions', 'position', 'preferred_email',
            'profile_key', 'profile_pic', 'push_token', 'read_anonymity',
            'school', 'signup_source', 'staff_type', 'start_year', 'state',
            'uni', 'unread_message_count', 'unread_notification_count', 'name',
            'vet_id', 'year_of_completion', 'total_pending_connections',
            'total_requested_connections', 'total_accepted_connections',
            'total_blocked_connections')
        read_only_fields = ('id', 'created')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """Allows user to POST which sets the password as well"""
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BlockedUserSerializer(serializers.ModelSerializer):
    blocked_user = UserSerializer()

    class Meta:
        model = BlockedUser
        fields = ('id', 'blocked_user')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileDetail
        fields = (
            'profile_type', 'profile_key', 'profile_value')


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ('created', 'email', 'code')
        read_only_fields = fields
