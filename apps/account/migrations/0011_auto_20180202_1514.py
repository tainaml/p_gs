# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-02 18:14
from __future__ import unicode_literals

import apps.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_user_gamification_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usertype',
            field=models.PositiveSmallIntegerField(default=1, validators=[apps.account.models.limit_usertypes_to], verbose_name='Tipo de usu\xe1rio'),
        ),
    ]
