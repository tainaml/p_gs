# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django_migration_fixture import fixture

from apps import contact


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(contact, ['initial_data.json'])),

    ]
