# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django_migration_fixture import fixture
from apps import configuration


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_auto_20151204_1642'),
    ]

    operations = [
        migrations.RunPython(**fixture(configuration, ['initial_data.json']))
    ]
