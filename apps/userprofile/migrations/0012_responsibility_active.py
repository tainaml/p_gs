# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20161102_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsibility',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]