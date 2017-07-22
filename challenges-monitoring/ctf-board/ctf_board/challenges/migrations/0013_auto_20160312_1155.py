# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 11:55
from __future__ import unicode_literals

import challenges.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0012_challenge_chall_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='chall_file',
            field=models.FileField(blank=True, max_length=4194304, null=True, upload_to=challenges.models.upload_path_chall_file),
        ),
    ]
