# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('universities', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('username', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('gender', models.CharField(default=None, max_length=6, null=True, blank=True, choices=[('male', 'male'), ('female', 'female'), ('other', 'other')])),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address', db_index=True)),
                ('email_secondary', models.CharField(max_length=254, null=True, blank=True)),
                ('prefered_email', models.CharField(default='primary', max_length=200, null=True, blank=True, choices=[('primary', 'primary'), ('secondary', 'secondary')])),
                ('vet_id', models.CharField(max_length=150, null=True, blank=True)),
                ('facebook_id', models.CharField(max_length=40, null=True, blank=True)),
                ('push_token', models.CharField(max_length=40, null=True, blank=True)),
                ('csu_id', models.CharField(max_length=40, null=True, blank=True)),
                ('profile_pic', models.CharField(max_length=255, null=True, blank=True)),
                ('cover_picture', models.CharField(max_length=200, null=True, blank=True)),
                ('signup_source', models.IntegerField(null=True, blank=True)),
                ('android_gcm', models.TextField(null=True, blank=True)),
                ('android_version', models.CharField(max_length=50, null=True, blank=True)),
                ('auth_token_mobile', models.CharField(max_length=255, null=True, blank=True)),
                ('campus_status', models.CharField(max_length=1, null=True, blank=True)),
                ('count_profile_views', models.IntegerField(null=True, blank=True)),
                ('hide_connection_info_popup', models.IntegerField(null=True, blank=True)),
                ('ios_apn_token', models.TextField(null=True, blank=True)),
                ('iphone_version', models.CharField(max_length=50, null=True, blank=True)),
                ('search_radius', models.IntegerField(null=True, blank=True)),
                ('start_year', models.IntegerField(null=True, blank=True)),
                ('unread_notifications', models.IntegerField(null=True, blank=True)),
                ('year_of_completion', models.IntegerField(null=True, blank=True)),
                ('finished', models.IntegerField(null=True, blank=True)),
                ('international', models.IntegerField(null=True, blank=True)),
                ('is_signed_flg', models.IntegerField(default=0)),
                ('is_vet', models.IntegerField(null=True, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=15, decimal_places=9, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=15, decimal_places=9, blank=True)),
                ('on_campus', models.BooleanField(default=False)),
                ('read_anonymity', models.IntegerField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('forgotten_password_code', models.CharField(max_length=40, null=True, blank=True)),
                ('remember_code', models.CharField(max_length=40, null=True, blank=True)),
                ('completed', models.IntegerField(null=True, blank=True)),
                ('attempt_fail', models.IntegerField(null=True, blank=True)),
                ('attempt_fail_date', models.DateTimeField(null=True, blank=True)),
                ('position', models.CharField(max_length=255, null=True, blank=True)),
                ('staff_type', models.CharField(max_length=100, null=True, blank=True)),
                ('deleted_data', models.TextField(null=True, blank=True)),
                ('parent_id', models.IntegerField(null=True, blank=True)),
                ('profile_key', models.CharField(max_length=500, null=True, blank=True)),
                ('profile_value', models.CharField(max_length=5000, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('campus', models.ForeignKey(blank=True, to='universities.Campus', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('blocked_user', models.ForeignKey(related_name='block_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonUcrooMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('first_name', models.CharField(max_length=50, null=True, blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.CharField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, to='users.Group', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='uni',
            field=models.ForeignKey(blank=True, to='universities.University', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
