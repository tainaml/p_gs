# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-31 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20171003_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='xp',
            field=models.BigIntegerField(default=0, verbose_name='XP'),
        ),
    ]
