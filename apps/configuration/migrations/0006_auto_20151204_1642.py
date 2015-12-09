# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django_migration_fixture import fixture
from apps import configuration

class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20151204_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(to='configuration.ConfigKey'),
        ),
        migrations.RunPython(**fixture(configuration, ['initial_data.json']))
    ]
