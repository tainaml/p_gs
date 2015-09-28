# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django_migration_fixture import fixture
from apps import taxonomy

class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0004_auto_20150922_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objecttaxonomy',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='objecttaxonomy',
            name='taxonomy',
        ),
        migrations.DeleteModel(
            name='ObjectTaxonomy',
        ),
        migrations.RunPython(**fixture(taxonomy, ['initial_data.json'])),
    ]
