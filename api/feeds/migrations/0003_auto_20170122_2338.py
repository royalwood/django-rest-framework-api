# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20170120_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='module_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='module_type',
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='feed_url',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='meta',
            field=models.TextField(null=True, blank=True),
        ),
    ]
