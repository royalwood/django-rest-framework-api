from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from actstream.models import Follow

from universities.serializers import CampusSerializer
from users.models import UserProfileDetail, UserProfileCategory
from users.serializers import UserSerializer
from .models import (
    Club, ClubMember, CustomGroup, CustomGroupMember, StudyGroup,
    StudyGroupMember, StudentService, StudentServiceAdmin, StudentServiceMember,
    StudentServiceEvent, StudentServiceEventMember, StudentServiceDropin,
    MentorGroup, MentorGroupMember, Event, EventMember)


class GroupSerializer(serializers.ModelSerializer):
    is_admin = SerializerMethodField()
    is_member = SerializerMethodField()
    is_following = SerializerMethodField()
    total_admins = SerializerMethodField()
    total_members = SerializerMethodField()
    total_following = SerializerMethodField()

    def get_is_admin(self, instance):
        return instance.is_admin(self.context['auth_user'])

    def get_is_member(self, instance):
        return instance.is_member(self.context['auth_user'])

    def get_is_following(self, instance):
        return Follow.objects.is_following(self.context['auth_user'], instance)

    def get_total_admins(self, instance):
        return instance.total_admins

    def get_total_members(self, instance):
        return instance.total_members

    def get_total_following(self, instance):
        return instance.total_following

    class Meta:
        fields = (
            'id', 'created', 'user', 'campus', 'school', 'name', 'description',
            'banner_pic', 'private', 'is_admin', 'is_member', 'is_following',
            'total_admins', 'total_members', 'total_followers')
        read_only_fields = (
            'id', 'created', 'user', 'is_admin', 'is_member', 'is_following',
            'total_admins', 'total_members', 'total_followers')


class JoinedGroupsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['clubs'] = ClubSerializer(ret['clubs'], many=True).data
        ret['customgroups'] = ClubSerializer(ret['customgroups'], many=True).data
        ret['studentservices'] = ClubSerializer(ret['studentservices'], many=True).data
        ret['studygroups'] = ClubSerializer(ret['studygroups'], many=True).data
        ret['mentorgroups'] = ClubSerializer(ret['mentorgroups'], many=True).data
        return ret


class ClubSerializer(GroupSerializer):
    class Meta:
        model = Club
        fields = GroupSerializer.Meta.fields
        read_only_fields = GroupSerializer.Meta.read_only_fields


class CustomGroupSerializer(GroupSerializer):
    class Meta(GroupSerializer.Meta):
        model = CustomGroup
        fields = GroupSerializer.Meta.fields + ('category',)
        read_only_fields = GroupSerializer.Meta.read_only_fields


class StudentServiceSerializer(GroupSerializer):
    class Meta:
        model = StudentService
        fields = GroupSerializer.Meta.fields + (
            'website', 'email', 'phone', 'member_message', 'office_location')
        read_only_fields = GroupSerializer.Meta.read_only_fields


class StudyGroupSerializer(GroupSerializer):
    class Meta:
        model = StudyGroup
        fields = GroupSerializer.Meta.fields + (
            'purpose', 'time_from', 'time_to', 'time_day')
        read_only_fields = GroupSerializer.Meta.read_only_fields


class MentorGroupSerializer(GroupSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        members_user = list(set(MentorGroupMember.objects.all().filter(group=instance).filter(types=1).values_list('user', flat=True)))
        ret['mentors'] = UserSerializer(get_user_model().objects.all().filter(id__in=members_user), many=True).data
        ret['mentor_programs'] = ret['program_name']
        ret['languages'] = list(set(UserProfileDetail.objects.all().filter(user__in=members_user).filter(profile_type=UserProfileCategory.objects.all().filter(profile_type='Language')).values_list('profile_value', flat=True)))
        ret['interest_hobby'] = list(set(UserProfileDetail.objects.all().filter(user__in=members_user).filter(profile_type=UserProfileCategory.objects.all().filter(profile_type='Interest')).values_list('profile_value', flat=True)))
        return ret

    class Meta:
        model = MentorGroup
        fields = GroupSerializer.Meta.fields + ('program_name',)
        read_only_fields = GroupSerializer.Meta.read_only_fields


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'created', 'user', 'group')
        read_only_fields = ('id', 'created', 'user')
        extra_kwargs = {
            'group': {'write_only': True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        return ret


class ClubMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = ClubMember
        fields = GroupMemberSerializer.Meta.fields + (
            'student_mobile', 'student_email', 'net_price', 'gst',
            'total_price', 'paid', 'membership_to', 'invoice', 'payment_type',
            'registration_type', 'payment_date')
        read_only_fields = GroupMemberSerializer.Meta.read_only_fields


class CustomGroupMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = CustomGroupMember
        fields = GroupMemberSerializer.Meta.fields
        read_only_fields = GroupMemberSerializer.Meta.read_only_fields


class StudentServiceMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = StudentServiceMember
        fields = GroupMemberSerializer.Meta.fields
        read_only_fields = GroupMemberSerializer.Meta.read_only_fields


class StudyGroupMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = StudyGroupMember
        fields = GroupMemberSerializer.Meta.fields
        read_only_fields = GroupMemberSerializer.Meta.read_only_fields


class MentorGroupMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = MentorGroupMember
        fields = GroupMemberSerializer.Meta.fields
        read_only_fields = GroupMemberSerializer.Meta.read_only_fields


class StudentServiceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentServiceAdmin
        fields = ('created', 'group', 'user', 'non_ucroo_id')
        read_only_fields = ('created',)


class StudentServiceEventSerializer(GroupMemberSerializer):
    class Meta:
        model = StudentServiceEvent
        fields = (
            'created', 'group', 'user', 'title', 'picture', 'picture_thumb',
            'start_date', 'end_date', 'location', 'max_attendees', 'campus',
            'timezone')
        read_only_fields = ('created',)


class StudentServiceEventMemberSerializer(GroupMemberSerializer):
    class Meta:
        model = StudentServiceEventMember
        fields = ('event', 'user', 'member_email')


class EventSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        ret['campus'] = CampusSerializer(instance.campus).data
        return ret

    class Meta:
        model = Event
        fields = (
            'created', 'user', 'uni', 'campus', 'module_id',
            'module_name', 'title', 'description', 'picture', 'picture_thumb',
            'start_date', 'end_date', 'target_year', 'location', 'timezone',
            'max_attendees')
        read_only_fields = ('created',)


class EventMemberSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        context = {'auth_user': self.context['auth_user']}
        ret['user'] = UserSerializer(instance.user, context=context).data
        return ret

    class Meta:
        model = EventMember
        fields = ('created', 'user', 'event')
        read_only_fields = ('created',)


class HappeningStudentServiceDropinSerializer(serializers.ModelSerializer):
    student_service = StudentServiceSerializer(read_only=True)
    student_service_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentService.objects.all(), source='student_service',
        write_only=True)

    class Meta:
        model = StudentServiceDropin
