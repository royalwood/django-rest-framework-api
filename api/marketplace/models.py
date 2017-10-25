from django.db import models
from django.db.models import Q
from django.conf import settings
from model_utils.models import TimeStampedModel
from actstream import action

from core.models import Category


class ItemManager(models.Manager):
    def search(self, query):
        return self.filter(title__icontains=query)


class Item(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Title is required
    title = models.TextField()
    # Description, can be blank
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=50, blank=True, null=True)
    # Related post? Remove this. No need for a post.
    feed_post_id = models.IntegerField(blank=True, null=True)
    # Category -- was "types" in old db
    category = models.ForeignKey(Category)
    # Use StatusModel mixin instead of this
    status = models.BooleanField(default=True)

    objects = ItemManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            # Save activity
            action.send(
                self.user, verb='posted marketplace item', action_object=self)
