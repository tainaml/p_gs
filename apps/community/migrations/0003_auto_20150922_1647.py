# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import community


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_load_intial_data'),
    ]

    operations = [
        migrations.RunPython(**fixture(community, ['initial_data.json'])),

    ]
