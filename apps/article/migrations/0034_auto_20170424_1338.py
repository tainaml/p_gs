# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-24 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0033_auto_20170220_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(max_length=100000),
        ),
    ]