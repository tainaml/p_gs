# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-01 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20160830_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='first_slug',
            field=models.SlugField(default=b'', max_length=255),
        ),
    ]