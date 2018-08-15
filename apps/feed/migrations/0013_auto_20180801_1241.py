# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-01 15:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0012_auto_20180323_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilestatus',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_status', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
