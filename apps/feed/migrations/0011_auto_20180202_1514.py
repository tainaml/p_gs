# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-02 18:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_auto_20171003_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilestatus',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_status', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
    ]
