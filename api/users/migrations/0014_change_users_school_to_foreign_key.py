# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_rename_faculty_to_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='school',
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='universities.School'),
        )
    ]