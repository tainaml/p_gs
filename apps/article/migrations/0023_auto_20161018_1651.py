# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 19:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0022_merge_20161017_1002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': [('change_other_articles', 'Can edit articles from others')]},
        ),
    ]
