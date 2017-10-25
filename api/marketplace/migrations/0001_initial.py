# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('types', models.IntegerField()),
                ('feed_post_id', models.IntegerField(null=True, blank=True)),
                ('item_name', models.TextField()),
                ('description', models.TextField()),
                ('image_name', models.CharField(max_length=50, null=True, blank=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('status', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, to='core.Category', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
