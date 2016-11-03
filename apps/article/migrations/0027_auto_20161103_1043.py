# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0026_auto_20161101_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='comment_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='dislike_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='like_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
