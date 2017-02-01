# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 17:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0022_auto_20170117_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsibility',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibilities', to=settings.AUTH_USER_MODEL),
        ),
    ]