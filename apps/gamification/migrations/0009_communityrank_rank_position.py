# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-13 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0008_auto_20180202_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityrank',
            name='rank_position',
            field=models.PositiveIntegerField(default=0, verbose_name='Position'),
        ),
    ]
