# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 19:43
from __future__ import unicode_literals

import apps.core.models.course
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_course_embed'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=apps.core.models.course.course_thumb_upload, verbose_name='Thumbnail'),
        ),
    ]
