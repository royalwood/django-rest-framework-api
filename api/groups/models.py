#pylint:disable=model-missing-unicode
from abc import ABCMeta, abstractmethod, abstractproperty

from django.db import models, transaction
from django.db.models import Q
from django.conf import settings
from model_utils.models import TimeStampedModel
from actstream import action
from actstream.actions import follow
from actstream.models import Follow

from universities.models import University, Campus, School
from users.models import NonMember
from core.models import Category
from feeds.settings import FEED_OBJECT_TYPES


class GroupManager(models.Manager):
    def search(self, query):
        return self.filter(
            Q(name__icontains=query) | Q(description__icontains=query))


class AbstractModelMeta(ABCMeta, type(models.Model)):
    """Allows models to be abstract classes. Could be moved into shared code
    somewhere to be used by others. Taken from
    https://gist.github.com/gavinwahl/7778717
    """
    pass


class Group(TimeStampedModel):
    __metaclass__ = AbstractModelMeta

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # was creator_user OR owner_user
    uni = models.ForeignKey(University)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    school = models.ForeignKey(School, blank=True, null=True)
    # non_ucroo_id - Get rid of this
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    banner_pic = models.CharField(max_length=200, blank=True, null=True)
    private = models.BooleanField(default=False)
    slug = models.CharField(max_length=100, blank=True, null=True)
    # count_views - remove this
    count_views = models.IntegerField(blank=True, null=True)

    objects = GroupManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or ''

    @abstractproperty
    def feed_object(self):
        """Return the FEED_OBJECT_TYPES for this group type"""

    # Admins
    @abstractmethod
    def add_admin(self, user):
        """Add an admin to the group"""

    @abstractmethod
    def remove_admin(self, user):
        """Remove an admin to the group"""

    @abstractmethod
    def is_admin(self, user):
        """Returns true if the specified user is an admin of the group"""

    @abstractproperty
    def total_admins(self):
        """Returns the number of admins in the group"""

    # Members
    @abstractmethod
    def remove_member(self, user):
        """Leave a group"""

    @abstractmethod
    def is_member(self, user):
        """Returns true if the specified user is a member of the group"""

    @abstractproperty
    def total_members(self):
        """Returns the number of members in the group"""

    @property
    def total_followers(self):
        """Returns the number of followers of the group"""
        return Follow.objects.for_object(self).count()

    @transaction.atomic
    def save(self, *args, **kwargs):
        creating = not self.pk
        ret = super().save(*args, **kwargs)
        if creating:
            # Creator auto-follows the group
            follow(self.user, self, actor_only=False)
        return ret


# Clubs & Societies
class Club(Group):
    short_name = models.CharField(max_length=10, blank=True)
    website = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    can_student_join = models.BooleanField(null=False, default=False)
    owner_position = models.CharField(max_length=100, blank=True, null=True)
    owner_manage_members = models.BooleanField(default=False)
    member_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    abn = models.CharField(max_length=20, blank=True, null=True)
    collect_gst = models.IntegerField(blank=True, null=True)
    digital_card = models.BooleanField(default=True)
    show_student_mobile = models.BooleanField(null=False, default=False)
    show_student_email = models.BooleanField(null=False, default=False)
    show_student_id = models.BooleanField(null=False, default=False)
    show_student_association = models.BooleanField(null=False, default=False)
    student_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    member_message = models.TextField(blank=True, null=True)
    thumbnail_pic = models.CharField(max_length=300, blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    eventbrite_id = models.CharField(max_length=255, blank=True, null=True)
    eventbrite_organizer_id = models.CharField(max_length=255, blank=True, null=True)
    eventbrite_token = models.CharField(max_length=255, blank=True, null=True)
    finished = models.BooleanField(default=False)
    is_marked_for_member_fields = models.CharField(max_length=1, blank=True, null=True)

    # These fields seems to be universally 'Y', there are no records with
    # anything else in them. So they're probably not being used. For now set the
    # default to 'Y'.
    membership_status = models.CharField(max_length=1, default='Y')
    membership_payment = models.CharField(max_length=1, default='Y')
    event_ticketing = models.CharField(max_length=1, default='Y')

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Set the creator to an admin
            self.add_admin(self.user)

    def __str__(self):
        return self.name

    @property
    def feed_object(self):
        return FEED_OBJECT_TYPES['CLUBS']

    # Admins
    def add_admin(self, user):
        # Ensure no duplicate entries
        admins = ClubAdmin.objects.filter(group=self, user=user)
        if not admins:
            return ClubAdmin.objects.create(group=self, user=user)

    def remove_admin(self, user):
        admins = ClubAdmin.objects.filter(group=self, user=user)
        if admins:
            admins.delete()

    def is_admin(self, user):
        """Returns true if the specified user is an admin of the group"""
        return ClubAdmin.objects.filter(group=self, user=user).exists()

    @property
    def total_admins(self):
        return ClubAdmin.objects.filter(group=self).count()

    # Members
    def remove_member(self, user):
        """Leave the group"""
        member = ClubMember.objects.filter(group=self, user=user)
        if member:
            member.delete()

    def is_member(self, user):
        """Returns true if the specified user is a member of the group"""
        return ClubMember.objects.filter(group=self, user=user).exists()

    @property
    def total_members(self):
        return ClubMember.objects.filter(group=self).count()


class CustomGroup(Group):
    category = models.ForeignKey(Category, blank=True, null=True)

    def __str__(self):
        return self.name or ''

    @property
    def feed_object(self):
        return FEED_OBJECT_TYPES['CUSTOMGROUPS']

    # Admins
    def add_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def remove_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def is_admin(self, user):
        # Customgroups don't have admins.
        return False

    @property
    def total_admins(self):
        return 0

    # Members
    def remove_member(self, user):
        member = CustomGroupMember.objects.filter(group=self, user=user)
        if member:
            member.delete()

    def is_member(self, user):
        return CustomGroupMember.objects.filter(group=self, user=user).exists()

    @property
    def total_members(self):
        return CustomGroupMember.objects.filter(group=self).count()


class StudentService(Group):
    website = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    member_message = models.TextField(blank=True, null=True)
    office_location = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Set the creator to an admin
            self.add_admin(self.user)

    @property
    def feed_object(self):
        return FEED_OBJECT_TYPES['STUDENTSERVICES']

    def __str__(self):
        return self.name

    # Admins
    def add_admin(self, user):
        # Ensure no duplicate entries
        admins = StudentServiceAdmin.objects.filter(group=self, user=user)
        if not admins:
            return StudentServiceAdmin.objects.create(group=self, user=user)

    def remove_admin(self, user):
        admins = StudentServiceAdmin.objects.filter(group=self, user=user)
        if admins:
            admins.delete()

    def is_admin(self, user):
        return StudentServiceAdmin.objects.filter(group=self, user=user).exists()

    @property
    def total_admins(self):
        return StudentServiceAdmin.objects.filter(group=self).count()

    # Members
    def remove_member(self, user):
        member = StudentServiceMember.objects.filter(group=self, user=user)
        if member:
            member.delete()

    def is_member(self, user):
        return StudentServiceMember.objects.filter(group=self, user=user).exists()

    @property
    def total_members(self):
        return StudentServiceMember.objects.filter(group=self.id).count()


class StudyGroup(Group):
    purpose = models.CharField(max_length=16, blank=True)
    time_from = models.TimeField()
    time_to = models.TimeField()
    # time_day - day of the week? seconds since 1970?
    time_day = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def feed_object(self):
        return FEED_OBJECT_TYPES['STUDYGROUPS']

    # Admins
    def add_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def remove_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def is_admin(self, user):
        return False

    @property
    def total_admins(self):
        return 0

    # Members
    def remove_member(self, user):
        """Leave the group"""
        member = StudyGroupMember.objects.filter(group=self, user=user)
        if member:
            member.delete()

    def is_member(self, user):
        """Returns true if the specified user is a member of the group"""
        return StudyGroupMember.objects.filter(group=self, user=user).exists()

    @property
    def total_members(self):
        return StudyGroupMember.objects.filter(group=self.id).count()


class MentorGroup(Group):
    # Program name is different to name.
    program_name = models.CharField(max_length=100, blank=True)
    find_mentor = models.SmallIntegerField(default=False)
    count_mentees = models.IntegerField(default=0)
    addable_mentees = models.IntegerField(default=False)

    def __str__(self):
        return '%s by %s' % (self.name, self.user.name)

    @property
    def feed_object(self):
        return FEED_OBJECT_TYPES['MENTORGROUPS']

    # Admins
    def add_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def remove_admin(self, user):
        raise NotImplementedError('These groups don\'t have admins')

    def is_admin(self, user):
        return False

    @property
    def total_admins(self):
        return 0

    # Members
    def remove_member(self, user):
        member = MentorGroupMember.objects.filter(group=self, user=user)
        if member:
            member.delete()

    def is_member(self, user):
        return MentorGroupMember.objects.filter(group=self, user=user).exists()

    @property
    def total_members(self):
        return MentorGroupMember.objects.filter(group=self.id).count()


class ClubAdminCommittee(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)
    club = models.ForeignKey(Club)
    position = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.name


class ClubAdmin(TimeStampedModel):
    group = models.ForeignKey(Club)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    manage_members = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.name


class ClubBank(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # creator
    last_modifier = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='last_modifier')
    club = models.ForeignKey(Club)
    bank_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    account_bsb = models.CharField(max_length=6)
    account_number = models.CharField(max_length=20)

    def __str__(self):
        return self.bank_name


class ClubEvent(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    club = models.ForeignKey(Club)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=200)
    picture = models.CharField(max_length=200, blank=True, null=True)
    picture_thumb = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    capacity = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.title


class ClubEventTicket(TimeStampedModel):
    event = models.ForeignKey(ClubEvent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  # was creator
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity_available = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    include_fee = models.IntegerField(blank=True, null=True)
    eventbrite_ticket_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.event.title


class ClubField(TimeStampedModel):
    club = models.ForeignKey(Club)
    label = models.CharField(max_length=255)
    field_order = models.IntegerField()

    def __str__(self):
        return self.label


class GroupMember(TimeStampedModel):
    """Make this properly abstract like Group"""
    # User is not required because of the whole non-ucroo-id thing, which we
    # should get rid of.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    # Remove this
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # The new member auto-follows the group
            follow(self.user, self.group, actor_only=False)
            action.send(self.user, verb='joined', action_object=self.group)


class ClubMember(GroupMember):
    group = models.ForeignKey(Club)
    gst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice = models.TextField(blank=True, null=True)
    is_card_generated = models.IntegerField(blank=True, null=True)
    membership_to = models.IntegerField(null=True)
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    registration_type = models.CharField(max_length=25, blank=True, null=True)
    student_association = models.IntegerField(blank=True, null=True)
    student_email = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    student_mobile = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)


class CustomGroupMember(GroupMember):
    group = models.ForeignKey(CustomGroup)
    # No need for email. Use user.email. Remove
    member_email = models.CharField(max_length=254, blank=True, null=True)
    # Not sure what it is, rename to type
    member_type = models.IntegerField(null=True)


class StudentServiceMember(GroupMember):
    group = models.ForeignKey(StudentService)
    student_email = models.CharField(max_length=254, blank=True, null=True)


class StudyGroupMember(GroupMember):
    group = models.ForeignKey(StudyGroup)
    # was invited_by_user_id
    invited_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='invited_by')


class MentorGroupMember(GroupMember):
    group = models.ForeignKey(MentorGroup)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)
    types = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name


class ClubMembersField(TimeStampedModel):
    club_member = models.ForeignKey(ClubMember)
    club_field = models.ForeignKey(ClubField)
    value = models.CharField(max_length=255)


class ClubNonUcrooMember(TimeStampedModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)


class StudentServiceAdmin(TimeStampedModel):
    group = models.ForeignKey(StudentService)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_ucroo_id = models.ForeignKey(NonMember, blank=True, null=True)

    def __str__(self):
        return '%s service admin of %s' % (self.user.name, self.group.name)


class StudentServiceDropin(TimeStampedModel):
    group = models.ForeignKey(StudentService)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    dropin_day = models.CharField(max_length=50)
    dropin_start = models.TimeField()
    dropin_end = models.TimeField()
    location = models.CharField(max_length=70, blank=True, null=True)

    def __str__(self):
        return self.group.name


class StudentServiceEvent(TimeStampedModel):
    group = models.ForeignKey(StudentService)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.CharField(max_length=200, blank=True, null=True)
    picture_thumb = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    max_attendees = models.CharField(max_length=5, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.group.name

    @property
    def total_members(self):
        return StudentServiceEventMember.objects.filter(event=self.id).count()


class StudentServiceEventMember(TimeStampedModel):
    event = models.ForeignKey(StudentServiceEvent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    member_email = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.event.title


# Events
class Event(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)  # was creator
    uni = models.ForeignKey(University, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    module_id = models.IntegerField()
    module_name = models.CharField(max_length=35)
    title = models.CharField(max_length=70)
    description = models.TextField()
    picture = models.CharField(max_length=100, blank=True, null=True)
    picture_thumb = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    target_year = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=100)
    timezone = models.CharField(max_length=75, blank=True, null=True)
    max_attendees = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return '%s Event at %s' % (self.title, self.uni.name)


class EventMember(TimeStampedModel):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    # member_email = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='member_email')

    def __str__(self):
        return self.user.name


class EventTicketSale(TimeStampedModel):
    club_event_ticket_id = models.IntegerField()
    no = models.IntegerField()
    paid = models.IntegerField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField()
    ticket_download_token = models.CharField(max_length=250, blank=True, null=True)
    ticket_send_by_mail = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
