# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-21 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0008_auto_20160312_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofile',
            name='on_site',
            field=models.BooleanField(default=False),
        ),
    ]