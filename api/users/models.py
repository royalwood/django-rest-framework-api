from django.db import models, transaction
from django.db.models import Q
from django.contrib.auth.models import (
    Group, BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.conf import settings
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from actstream.actions import follow, unfollow

from conversations.models import Message
from karma.models import History
#from notifications.models import Notification
from universities.models import University, Campus, School, Course


GENDER_CHOICES = [('male', 'male'), ('female', 'female'), ('other', 'other'),
    ('prefer not to say', 'prefer not to say')]
PREFERRED_EMAIL_CHOICES = [('primary', 'primary'), ('secondary', 'secondary')]


class Connection(TimeStampedModel, StatusModel):
    # Statuses used by the StatusModel mixin
    STATUS = Choices('pending', 'accepted', 'blocked')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='them')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='me')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.name} {self.status} {self.to_user.name}'


# Custom User Manger + Model
class UserManager(BaseUserManager):
    def _create_user(self, uni, email, password, **kwargs):
        user = self.model(uni=uni, email=UserManager.normalize_email(email), **kwargs)
        user.set_password(password)
        return user

    def create_user(self, uni, email, password='ucroo123', group_name=None, **kwargs):
        user = self._create_user(uni, email, password, **kwargs)
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        user.save()
        return user

    def create_superuser(self, uni, email, password='ucroo123', **kwargs):
        user = self._create_user(uni, email, password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def search(self, query):
        return self.filter(
            Q(name__icontains=query) | Q(email__icontains=query))


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    uni = models.ForeignKey(University)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    school = models.ForeignKey(School, null=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    email_secondary = models.CharField(max_length=254, blank=True, null=True)
    preferred_email = models.CharField(
        choices=PREFERRED_EMAIL_CHOICES, default='primary', max_length=200,
        null=True, blank=True)
    name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        default=None, choices=GENDER_CHOICES, max_length=6, null=True,
        blank=True)
    vet_id = models.CharField(max_length=150, blank=True, null=True)
    facebook_id = models.CharField(max_length=40, blank=True, null=True)
    push_token = models.CharField(max_length=40, blank=True, null=True)
    csu_id = models.CharField(max_length=40, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    banner_pic = models.CharField(max_length=200, blank=True, null=True)
    signup_source = models.IntegerField(blank=True, null=True)
    # merged 'user_meta' table; some fields ordered above
    android_gcm = models.TextField(blank=True, null=True)
    android_version = models.CharField(max_length=50, blank=True, null=True)
    auth_token_mobile = models.CharField(max_length=255, blank=True, null=True)
    campus_status = models.CharField(max_length=1, blank=True, null=True)
    count_profile_views = models.IntegerField(blank=True, null=True)
    hide_connection_info_popup = models.IntegerField(blank=True, null=True)
    ios_apn_token = models.TextField(blank=True, null=True)
    iphone_version = models.CharField(max_length=50, blank=True, null=True)
    search_radius = models.IntegerField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    year_of_completion = models.IntegerField(blank=True, null=True)
    # merged 'user_transaction' table
    finished = models.IntegerField(blank=True, null=True)
    international = models.IntegerField(blank=True, null=True)
    is_signed_flg = models.IntegerField(default=0)
    is_vet = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=9, blank=True, null=True)
    on_campus = models.BooleanField(default=False)
    read_anonymity = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    # Merged in from user_extra
    attempt_fail = models.IntegerField(blank=True, null=True)
    attempt_fail_date = models.DateTimeField(blank=True, null=True)
    completed = models.IntegerField(blank=True, null=True)
    deleted_data = models.TextField(blank=True, null=True)
    forgotten_password_code = models.CharField(max_length=40, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    remember_code = models.CharField(max_length=40, blank=True, null=True)
    staff_type = models.CharField(max_length=100, blank=True, null=True)
    # Merged in from user_profile_detail. Not sure what parent_id is
    parent_id = models.IntegerField(blank=True, null=True)
    profile_key = models.CharField(max_length=500, blank=True, null=True)
    profile_value = models.CharField(max_length=5000, blank=True, null=True)
    # Statuses
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    #Account Settings
    email_notifications = models.BooleanField(default=True)
    # Connections
    # See http://charlesleifer.com/blog/self-referencing-many-many-through/
    connections = models.ManyToManyField(
        'self', through='Connection', symmetrical=False,
        related_name='connected_to+')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        ordering = ('created',)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_full_name(self):
        """Required for admin"""
        return self.name

    def get_short_name(self):
        """Required for admin"""
        return self.name

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Follow all-students feed - can no longer do this, because we can
            # only follow something that has a record in the db. Need to add a
            # feeds table so there's a record to follow.
            pass

    # Connections. When adding a connection, the person sending has a
    # relationship of "accepted", but the reverse relationship's status is just
    # "pending".
    # http://charlesleifer.com/blog/self-referencing-many-many-through/
    @transaction.atomic
    def add_connection(self, user):
        # Create connection if not already exists
        connection = Connection.objects.update_or_create(
            from_user=self, to_user=user,
            defaults={'status': Connection.STATUS.accepted})
        # Also add the reverse relationship - only if it doesn't exist, because
        # the other use might already have "blocked".
        try:
            Connection.objects.get(from_user=user, to_user=self)
        except Connection.DoesNotExist:
            Connection.objects.create(
                from_user=user, to_user=self,
                status=Connection.STATUS.pending)
        # Follow the user
        follow(self, user)
        return connection

    # Connections. When adding a connection, the person sending has a
    # relationship of "accepted", but the reverse relationship's status is just
    # "pending".
    # http://charlesleifer.com/blog/self-referencing-many-many-through/
    @transaction.atomic
    def block_connection(self, user):
        # Create connection if not already exists
        connection = Connection.objects.update_or_create(
            from_user=self, to_user=user,
            defaults={'status': Connection.STATUS.blocked})
        # Unfollow the user
        unfollow(self, user)
        return connection

    @transaction.atomic
    def remove_connection(self, user):
        # Remove the connection
        connection = Connection.objects.filter(from_user=self, to_user=user)
        connection.delete()
        # Also remove the reverse relationship
        connection = Connection.objects.filter(from_user=user, to_user=self)
        # Don't remove "block" connections. Blocks should remain until the
        # unblock endpoint is called.
        connection = connection.exclude(status=Connection.STATUS.blocked)
        connection.delete()
        # Unfollow the user (but don't make the other user unfollow)
        unfollow(self, user)

    def get_connections(self):
        """Get connections from me"""
        return self.connections.filter(me__from_user=self)

    def get_pending_connections(self):
        """Get connections who the user has not yet accepted."""
        return self.get_connections().filter(
            me__status=Connection.STATUS.pending)

    def get_requested_connections(self):
        """Get connections this user has requested, but the other user has not
        yet accepted.
        """
        connections = self.get_connections().filter(
            me__status=Connection.STATUS.accepted)
        connections = connections.exclude(
            them__status=Connection.STATUS.accepted)
        return connections

    def get_accepted_connections(self):
        """Get connections who are "accepted" in both directions."""
        return self.get_connections().filter(
            me__status=Connection.STATUS.accepted,
            them__status=Connection.STATUS.accepted)

    def get_blocked_connections(self):
        """Get connections the user has blocked"""
        return self.get_connections().filter(
            me__status=Connection.STATUS.blocked)

    def is_connected(self, user):
        return self.connections.filter(
            me__from_user=self, me__to_user=user,
            me__status=Connection.STATUS.accepted,
            them__status=Connection.STATUS.accepted).exists()

    def get_connection_status(self, user):
        """Returns true if self is connected to user, and the reverse
        relationship is pending
        """
        try:
            me = Connection.objects.get(from_user=self, to_user=user)
            # Is my status blocked? (May not have a return relation)
            if me.status == Connection.STATUS.blocked:
                return me.status
            them = Connection.objects.get(from_user=user, to_user=self)
        except:
            return 'disconnected'
        # My status must be "accepted". Have they accepted?
        if me.status == Connection.STATUS.pending:
            return Connection.STATUS.pending
        if them.status == Connection.STATUS.accepted:
            return Connection.STATUS.accepted
        else:
            return 'requested'

    @property
    def total_pending_connections(self):
        return self.get_pending_connections().count()

    @property
    def total_requested_connections(self):
        return self.get_requested_connections().count()

    @property
    def total_accepted_connections(self):
        return self.get_accepted_connections().count()

    @property
    def total_blocked_connections(self):
        return self.get_blocked_connections().count()

    # total karma points
    # https://ucroo.zendesk.com/hc/en-us/articles/203761039-Earning-Points-and-your-Avatar
    # avatar is redundant
    def cumulated_karma_points(self):
        return History.objects.filter(user=self.id).aggregate(total_karma_points=models.Sum('points'))

    def unread_message_count(self):
        return 0 #Message.objects.filter(user=self.id).filter(is_read=False).count()

    def unread_notification_count(self):
        return 0 #Notification.objects.filter(user=self.id).filter(is_read=False).count()


class NonMember(TimeStampedModel):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=254)
    # merged table 'service_non_ucroo_member'
    # student_service_id = models.ForeignKey(StudentService, blank=True, null=True)

    def __str__(self):
        return self.email


class BlockedUser(TimeStampedModel):
    user = models.ForeignKey(User)
    blocked_user = models.ForeignKey(User, related_name="block_user")

    def __str__(self):
        return '%s blocking %s' % (self.user.name, self.blocked_user.name)


class UserProfileCategory(TimeStampedModel):
    profile_type = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.profile_type


class UserProfileDetail(TimeStampedModel):
    old_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)  # was user_id
    parent_id = models.IntegerField()
    # profile_type = models.CharField(max_length=500, blank=True, null=True)
    profile_type = models.ForeignKey(UserProfileCategory, blank=True, null=True)
    profile_key = models.CharField(max_length=500, blank=True, null=True)
    profile_value = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.user.name


class VerificationCode(TimeStampedModel):
    email = models.CharField(default=0, max_length=200, null=False)
    code = models.CharField(default=0, max_length=200, null=False)

    def __str__(self):
        return 'Verification for %s' % self.email
