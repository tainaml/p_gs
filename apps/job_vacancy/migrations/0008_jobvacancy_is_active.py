# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-18 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0007_jobvacancyadditionalrequirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobvacancy',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='A\xe7\xe3o'),
        ),
    ]
