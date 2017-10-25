# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_time', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField()),
                ('total_minutes', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=1)),
                ('subject', models.ForeignKey(blank=True, to='subjects.Subject', null=True)),
                ('uni', models.ForeignKey(to='universities.University')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
