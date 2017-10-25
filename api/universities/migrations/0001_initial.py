# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=300, null=True, blank=True)),
                ('timezone', models.CharField(max_length=300)),
                ('latitude', models.CharField(max_length=300)),
                ('longitude', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('live_id', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('code', models.CharField(max_length=5)),
                ('state', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('aff_token', models.CharField(max_length=255, null=True, blank=True)),
                ('app_key', models.CharField(max_length=255, null=True, blank=True)),
                ('secret_key', models.CharField(max_length=255, null=True, blank=True)),
                ('policy', models.TextField(null=True, blank=True)),
                ('side_menu', jsonfield.fields.JSONField(default='[{"location":"club", "title":"Clubs & Societies"},{"location":"unit", "title":"Subjects"},{"location":"study_group", "title":"Study"},{"location":"service_page", "title":"Student Services"},{"location":"mentors", "title":"Mentors"},{"location":"customgroups", "title":"Custom"}]')),
                ('aaf', models.BooleanField(default=False)),
                ('sign_up', models.BooleanField(default=True)),
                ('lti_key', models.CharField(max_length=255, null=True)),
                ('lti_secret', models.CharField(max_length=255, null=True)),
                ('lti_context_id', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='faculty',
            name='uni',
            field=models.ForeignKey(blank=True, to='universities.University', null=True),
        ),
        migrations.AddField(
            model_name='campus',
            name='uni',
            field=models.ForeignKey(to='universities.University'),
        ),
    ]
