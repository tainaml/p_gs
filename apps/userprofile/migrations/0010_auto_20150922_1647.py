# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import userprofile


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_merge'),
    ]

    operations = [
        migrations.RunPython(**fixture(userprofile, ['initial_data.json'])),

    ]
