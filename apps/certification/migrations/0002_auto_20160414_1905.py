# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
