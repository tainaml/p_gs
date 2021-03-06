# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-01 15:41
from __future__ import unicode_literals

import apps.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20180202_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usertype',
            field=models.PositiveSmallIntegerField(default=1, validators=[apps.account.models.limit_usertypes_to], verbose_name='User type'),
        ),
    ]
