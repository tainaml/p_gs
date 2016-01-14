# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django_migration_fixture import fixture

from apps import article


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(article, ['initial_data.json'])),

    ]
