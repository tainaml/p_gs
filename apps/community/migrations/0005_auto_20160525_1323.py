# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-25 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.TextField(),
        ),
    ]
