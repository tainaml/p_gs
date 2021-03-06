# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-29 18:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_auto_20160525_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configkey',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_keys', to='configuration.ConfigGroup', verbose_name='Configs Keys'),
        ),
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_values', to='configuration.ConfigKey', verbose_name='Config Values'),
        ),
    ]
