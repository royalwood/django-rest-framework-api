from django.db import models, transaction
from django.conf import settings
from django.utils.html import strip_tags
from rest_framework.reverse import reverse
from model_utils.models import TimeStampedModel, StatusModel, SoftDeletableModel
from model_utils import Choices, FieldTracker
from html2text import html2text
from actstream import action
from actstream.actions import follow

from universities.models import University, Campus, School, Course
from keywords.models import Keyword


class Post(TimeStampedModel, StatusModel, SoftDeletableModel):
    # Statuses used by the StatusModel mixin
    STATUS = Choices('posted', 'reported', 'cleared')

    # The author/creator of the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    # The feed it should go into. (These should be a foreign key to a feeds
    # table.)
    feed_object = models.CharField(max_length=16)
    feed_object_id = models.IntegerField()

    # Type: Usually 'post', but might be "event".
    type = models.CharField(max_length=12, blank=True, null=True, default='post')
    # This relates to the above "type". For regular posts, it's usually null.
    # For events, it's the event id.
    feed_posts_meta_id = models.IntegerField(null=True)

    # Targeting. Uni is required, the others are optional.
    uni = models.ForeignKey(University)
    course = models.ForeignKey(Course, blank=True, null=True)
    school = models.ForeignKey(School, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)

    # Merged from feed_post_meta
    title = models.CharField(max_length=100, blank=True, null=True)
    # Description is not being used according to @trezoid. (Plenty of records
    # have populated so keep it for now.)
    description = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True) # Remove this
    # Rename to permalink
    feed_url = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    fb_page_id = models.CharField(max_length=100, blank=True, null=True)

    # Was content
    body = models.TextField()

    # Moderation status and other flags
    is_attachment = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_international = models.NullBooleanField(default=False, blank=True, null=True)

    # Statistics
    views = models.IntegerField(default=0, blank=True, null=True)
    likes_count = models.IntegerField(default=0)

    # Targeting all students posts
    targeting = models.TextField(blank=True, null=True)

    # Dates
    year = models.IntegerField(blank=True, null=True)
    scheduled_start_date = models.DateTimeField(blank=True, null=True)
    scheduled_end_date = models.DateTimeField(blank=True, null=True)
    deleted_datetime = models.DateTimeField(blank=True, null=True)
    pinning_date = models.DateTimeField(blank=True, null=True)

    is_removed_tracker = FieldTracker(fields=['is_removed'])

    def __str__(self):
        return self.title or ''

    @property
    def body_plain(self):
        """Returns the plain-text version of the 'body' field."""
        return strip_tags(self.body)

    @property
    def body_markdown(self):
        """Returns the markdown version of the 'body' field. Eventually the
        body being stored will be markdown. But for now it's html, so we should
        convert the stored body to markdown.
        """
        return html2text(self.body)

    @property
    def body_html(self):
        """Returns the html version of the body field. Currently the stored
        version of the post is html.
        """
        return self.body

    @property
    def total_comments(self):
        return Comment.objects.count(self)

    @transaction.atomic
    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Add a log entry as 'posted'.
            PostLog.objects.create(
                post=self, user=self.user, status=Post.STATUS.posted)
            # Add Karma
            if self.feed_object == 'subject':
                History.objects.create(
                    user=self.user, points=5, points_type=None,
                    description='class question asked')
            # Check keywords
            Keyword.objects.notify(
                self.user.uni, '{} {}'.format(self.title, self.body),
                reverse('api:posts-detail', args=[self.pk]))
            # Poster should follow this post (to get "x commented on your post")
            follow(self.user, self, actor_only=False)
            # If posting in a group's feed, save activity.
            from groups.models import (
                Club, CustomGroup, StudentService, StudyGroup, MentorGroup)
            GROUP_FEED_OBJECT_TYPES = {
                'club': Club,
                'customgroups': CustomGroup,
                'service_page': StudentService,
                'study_group': StudyGroup,
                'mentors': MentorGroup,
            }
            group_cls = GROUP_FEED_OBJECT_TYPES.get(self.feed_object)
            # Posting in one of the group feeds?
            if group_cls:
                # The group should exist since it was checked in
                # serializer.validate()
                group = group_cls.objects.get(pk=self.feed_object_id)
                action.send(
                    self.user, verb='posted', action_object=self, target=group)

    def report(self, user, comment=''):
        self.status = self.STATUS.reported
        self.save()
        PostLog.objects.create(
            post=self, user=user, status=PostLog.STATUS.reported,
            comment=comment)

    def clear(self, user, comment=''):
        self.status = self.STATUS.cleared
        self.save()
        PostLog.objects.create(
            post=self, user=user, status=PostLog.STATUS.cleared,
            comment=comment)

    def first_comments(self):
        return self.comment_set.order_by('-created')[:5]


class CommentManager(models.Manager):
    def count(self, post):
        """Returns the total number of comments in a post"""
        ret = self.filter(post=post).count()
        return ret


class Comment(TimeStampedModel):
    """A comment on a post. Chase mentioned he wants heirarchical comments
    eventually, maybe look at django-mptt.
    """
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    # Replace this with StatusModel
    status = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Check keywords
            Keyword.objects.notify(
                self.user.uni, self.text,
                reverse('api:posts-detail', args=[self.pk]))
            # Commenting auto-follows the post
            follow(self.user, self.post, actor_only=False)
            # Save activity
            action.send(
                self.user, verb='commented', action_object=self,
                target=self.post)

class PostLog(TimeStampedModel, StatusModel):
    """A report on a post. Was ucroo_feed_reported in the old db. Here we record
    various actions on the post being moderated.
    """
    # The type of moderation being actioned.
    STATUS = Choices('posted', 'edited', 'reported', 'cleared', 'removed')
    # The user who is performing the action.
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The post being moderated or reported.
    post = models.ForeignKey(Post)
    # Comment on the action (optional). For example, a reporter might explain
    # why they're reporting the post.
    comment = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.post.title or 'No title'


class PostTag(TimeStampedModel):
    post = models.ForeignKey(Post)
    tag = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.tag


class PostAttachment(TimeStampedModel):
    post = models.ForeignKey(Post)
    attachment_id = models.IntegerField() # What's the point of this? Primary key?

    def __str__(self):
        return self.attachment_id


class PollAnswer(TimeStampedModel):
    post = models.ForeignKey(Post)
    answer = models.CharField(max_length=256)

    def __str__(self):
        return self.answer


# Is this anything? It's not being used currently
class PostType(TimeStampedModel):
    type_name = models.CharField(max_length=100)
    status = models.IntegerField()

    def __str__(self):
        return self.type_name


class Rss(TimeStampedModel):
    gu_id = models.CharField(unique=True, max_length=250)
    title = models.CharField(max_length=100)
    content = models.TextField()
    link = models.CharField(max_length=250)
    media = models.CharField(max_length=250)
    processed = models.TextField()
    type = models.CharField(max_length=4)
    date_fetch = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.link
