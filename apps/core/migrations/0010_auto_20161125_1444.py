# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 17:44
from __future__ import unicode_literals

import apps.core.models.course
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20161125_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, upload_to=apps.core.models.course.course_image_upload, verbose_name='Image'),
        ),
    ]
