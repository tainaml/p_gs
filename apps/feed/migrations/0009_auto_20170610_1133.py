# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-10 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20170216_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='seo_no_follow',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='feedobject',
            name='seo_no_index',
            field=models.BooleanField(default=True),
        ),
    ]
