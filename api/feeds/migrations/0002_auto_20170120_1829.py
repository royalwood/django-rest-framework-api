# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universities', '0001_initial'),
        ('subjects', '0002_auto_20170120_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportedpost',
            name='reporter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posttag',
            name='post',
            field=models.ForeignKey(to='feeds.Post'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(to='feeds.Post'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postattachment',
            name='post',
            field=models.ForeignKey(to='feeds.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_campus',
            field=models.ForeignKey(blank=True, to='universities.Campus', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_faculty',
            field=models.ForeignKey(blank=True, to='universities.School', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_uni',
            field=models.ForeignKey(to='universities.University'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pollanswer',
            name='post',
            field=models.ForeignKey(to='feeds.Post'),
        ),
        migrations.AddField(
            model_name='follower',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
