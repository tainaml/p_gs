# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0014_auto_20160920_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='image',
            field=models.ImageField(blank=True, upload_to=b'community/%Y/%m/%d'),
        ),
    ]