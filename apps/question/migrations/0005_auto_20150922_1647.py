# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import question


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_auto_20150914_1015'),
    ]

    operations = [
        migrations.RunPython(**fixture(question, ['initial_data.json'])),

    ]
