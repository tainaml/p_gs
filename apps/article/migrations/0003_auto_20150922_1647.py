# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import article


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20150901_2029'),
    ]

    operations = [
        migrations.RunPython(**fixture(article, ['initial_data.json'])),

    ]
