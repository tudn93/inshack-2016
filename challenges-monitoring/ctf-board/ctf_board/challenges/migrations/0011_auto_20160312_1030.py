# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0010_ctfsettings'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teamflagchall',
            unique_together=set([('flagger', 'chall')]),
        ),
    ]