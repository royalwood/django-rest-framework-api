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
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('type', models.CharField(max_length=12)),
                ('class_type', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=1000, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('time_from', models.TimeField(null=True, blank=True)),
                ('time_to', models.TimeField(null=True, blank=True)),
                ('time_day', models.IntegerField()),
                ('is_all_day_event', models.BooleanField(default=False)),
                ('color', models.CharField(max_length=200, null=True, blank=True)),
                ('by_academic', models.IntegerField(null=True, blank=True)),
                ('recurring_rule', models.CharField(max_length=11, null=True, blank=True)),
                ('assessment_date', models.DateField(null=True, blank=True)),
                ('assessment_time', models.TimeField(null=True, blank=True)),
                ('assessment_alert', models.DateField(null=True, blank=True)),
                ('event_cal_type', models.CharField(max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
