# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonomy',
            name='update_in',
            field=models.DateTimeField(auto_now=True),
        ),
    ]