# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import comment


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_comment_level'),
    ]

    operations = [
        migrations.RunPython(**fixture(comment, ['initial_data.json'])),

    ]
