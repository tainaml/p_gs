# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-10 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0005_auto_20160509_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobvacancy',
            name='description',
        ),
    ]
