# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-05 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_auto_20160204_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='category',
            field=models.CharField(choices=[('STG', 'Stéganographie'), ('WBS', 'Web serveur'), ('WBC', 'Web client'), ('CRK', 'Cracking'), ('PRG', 'Programmation'), ('RES', 'Réseau'), ('CRY', 'Cryptographie')], default='WBS', max_length=3),
        ),
    ]