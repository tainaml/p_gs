# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-06 17:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0024_auto_20170104_1059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'company')]),
        ),
    ]
