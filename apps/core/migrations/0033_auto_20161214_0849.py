# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-14 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_course_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='Avalia\xe7\xe3o'),
        ),
    ]
