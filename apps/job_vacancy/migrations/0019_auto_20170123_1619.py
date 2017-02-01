# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-23 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0018_auto_20170120_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Taxonomy', verbose_name='Item'),
        ),
    ]