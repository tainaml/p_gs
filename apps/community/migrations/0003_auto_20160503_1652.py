# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20160414_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='related_community', to='community.Community', verbose_name='Comunidade relacionada'),
        ),
    ]