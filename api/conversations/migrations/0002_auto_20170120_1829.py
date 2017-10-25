# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(to='conversations.Message'),
        ),
    ]
