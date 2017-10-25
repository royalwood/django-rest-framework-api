# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universities', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='non_ucroo',
            field=models.ForeignKey(blank=True, to='users.NonUcrooMember', null=True),
        ),
        migrations.AddField(
            model_name='keyword',
            name='uni',
            field=models.ForeignKey(to='universities.University'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
