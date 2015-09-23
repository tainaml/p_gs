# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
from apps import account


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20150825_2227'),
    ]

    operations = [
        #migrations.RunPython(**fixture(account, ['initial_data.json'])),

    ]
