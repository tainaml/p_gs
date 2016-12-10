# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 13:26
from __future__ import unicode_literals

import apps.account.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_usertype'),
        ('core', '0005_auto_20160929_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('account.user',),
            managers=[
                ('objects', apps.account.manager.UserManager()),
            ],
        ),
    ]