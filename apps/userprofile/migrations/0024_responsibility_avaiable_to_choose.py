# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0023_responsibility_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsibility',
            name='avaiable_to_choose',
            field=models.BooleanField(default=True, verbose_name='Avaiable'),
        ),
    ]