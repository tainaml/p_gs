# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-16 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20170314_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(max_length=400, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descri\xe7\xe3o'),
        ),
    ]
