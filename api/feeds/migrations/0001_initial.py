# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('feed_object', models.CharField(max_length=16)),
                ('feed_object_id', models.IntegerField()),
                ('last_id', models.IntegerField()),
                ('subscribed', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('answer', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('feed_object', models.CharField(max_length=16)),
                ('feed_object_id', models.IntegerField()),
                ('type', models.CharField(max_length=12, null=True, blank=True)),
                ('post_year', models.IntegerField(null=True, blank=True)),
                ('content', models.TextField()),
                ('html', models.TextField(null=True, blank=True)),
                ('is_attachment', models.BooleanField(default=False)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0, null=True, blank=True)),
                ('likes_count', models.IntegerField(default=0)),
                ('tags', models.TextField(null=True, blank=True)),
                ('post_is_international', models.NullBooleanField(default=False)),
                ('post_fb_page_id', models.CharField(max_length=100, null=True, blank=True)),
                ('pinning_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('scheduled_start_date', models.DateTimeField(null=True, blank=True)),
                ('scheduled_end_date', models.DateTimeField(null=True, blank=True)),
                ('module_type', models.CharField(max_length=256)),
                ('module_id', models.IntegerField()),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('meta', models.TextField()),
                ('feed_url', models.TextField()),
                ('description', models.TextField()),
                ('deleted_datetime', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('attachment_id', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('comment', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('is_anonymous', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('type_name', models.CharField(max_length=100)),
                ('status', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('flag', models.SmallIntegerField()),
                ('post', models.ForeignKey(to='feeds.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('gu_id', models.CharField(unique=True, max_length=250)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('link', models.CharField(max_length=250)),
                ('media', models.CharField(max_length=250)),
                ('processed', models.TextField()),
                ('type', models.CharField(max_length=4)),
                ('date_fetch', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
