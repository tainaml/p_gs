# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-24 14:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0019_auto_20170123_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobvacancy',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, message='Apenas n\xfameros maiores que 1 s\xe3o permitidos')], verbose_name='Quantidade'),
        ),
    ]
