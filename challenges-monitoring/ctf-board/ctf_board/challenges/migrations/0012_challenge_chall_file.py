# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 11:44
from __future__ import unicode_literals

import challenges.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0011_auto_20160312_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='chall_file',
            field=models.ImageField(blank=True, null=True, upload_to=challenges.models.upload_path_chall_file),
        ),
    ]
