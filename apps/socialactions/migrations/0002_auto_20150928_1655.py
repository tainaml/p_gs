# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django_migration_fixture import fixture

from apps import socialactions


class Migration(migrations.Migration):

    dependencies = [
        ('socialactions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(socialactions, ['initial_data.json'])),

    ]
