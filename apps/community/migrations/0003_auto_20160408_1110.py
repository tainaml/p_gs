# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20160401_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='related_community', to='community.Community', verbose_name='Community Related'),
        ),
    ]
