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
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('course_code', models.CharField(max_length=100)),
                ('live_id', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('code', models.CharField(max_length=20, null=True, blank=True)),
                ('year', models.IntegerField()),
                ('search', models.CharField(max_length=150)),
                ('added_user_type', models.CharField(max_length=25)),
                ('subject_code', models.CharField(max_length=25, null=True, blank=True)),
                ('activity_number', models.CharField(max_length=25, null=True, blank=True)),
                ('subject_title', models.CharField(max_length=250, null=True, blank=True)),
                ('day', models.CharField(max_length=10, null=True, blank=True)),
                ('time', models.TimeField()),
                ('duration', models.DecimalField(max_digits=4, decimal_places=2)),
                ('subject_type', models.CharField(max_length=250, null=True, blank=True)),
                ('class_type', models.CharField(max_length=25, null=True, blank=True)),
                ('location', models.CharField(max_length=25, null=True, blank=True)),
                ('staff', models.CharField(max_length=250, null=True, blank=True)),
                ('semester', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectEnrollee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('non_ucroo_id', models.IntegerField(null=True, blank=True)),
                ('semester', models.IntegerField(null=True, blank=True)),
                ('year', models.IntegerField()),
                ('subject', models.ForeignKey(to='subjects.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('feed_object', models.CharField(max_length=16)),
                ('feed_object_id', models.IntegerField()),
                ('title', models.CharField(max_length=300)),
                ('sort_order', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
