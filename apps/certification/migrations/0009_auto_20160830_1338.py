# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-30 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0008_auto_20160822_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='title',
            field=models.CharField(max_length=100, verbose_name='T\xedtulo'),
        ),
    ]
