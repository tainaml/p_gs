# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='responsibility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occupation', to='userprofile.Responsibility'),
        ),
    ]
