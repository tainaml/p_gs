# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0013_auto_20160919_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='related_community', to='community.Community', verbose_name='Comunidade relacionada'),
        ),
    ]
