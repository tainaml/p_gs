# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-10 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20160509_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.CharField(default=1, max_length=255, verbose_name='Descri\xe7\xe3o'),
            preserve_default=False,
        ),
    ]