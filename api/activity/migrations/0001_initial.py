# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=40, null=True, blank=True)),
                ('entity_id', models.IntegerField(null=True, blank=True)),
                ('entity_type', models.CharField(max_length=40, null=True, blank=True)),
                ('entity_extra', models.CharField(max_length=40, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'activity',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActivityTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_id', models.IntegerField(null=True, blank=True)),
                ('is_read', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('activity', models.ForeignKey(to='activity.Activity')),
                ('user_to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'activity_transaction',
                'managed': True,
            },
        ),
    ]
