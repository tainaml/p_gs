# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-30 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20160525_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=b'', max_length=255),
        ),
    ]
