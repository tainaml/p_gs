# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import taxonomy


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_auto_20150910_1337'),
    ]

    operations = [
        migrations.RunPython(**fixture(taxonomy, ['initial_data.json'])),

    ]
