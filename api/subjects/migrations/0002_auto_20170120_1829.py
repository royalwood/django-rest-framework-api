# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universities', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectenrollee',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='added_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='campus',
            field=models.ForeignKey(to='universities.Campus'),
        ),
        migrations.AddField(
            model_name='subject',
            name='uni',
            field=models.ForeignKey(to='universities.University'),
        ),
        migrations.AddField(
            model_name='course',
            name='uni',
            field=models.ForeignKey(blank=True, to='universities.University', null=True),
        ),
    ]
