# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-02 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_auto_20161101_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsibility',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
