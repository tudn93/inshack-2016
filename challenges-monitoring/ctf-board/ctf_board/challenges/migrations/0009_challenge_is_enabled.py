# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0008_auto_20160207_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
