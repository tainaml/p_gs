# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-27 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0003_auto_20171027_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communityrank',
            old_name='communitiy',
            new_name='community',
        ),
    ]
