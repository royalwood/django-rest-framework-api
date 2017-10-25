# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentcalendar', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='unit',
            field=models.ForeignKey(blank=True, to='subjects.Subject', null=True),
        ),
    ]
