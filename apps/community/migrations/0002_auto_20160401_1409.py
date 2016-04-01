# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 17:09
from __future__ import unicode_literals

from django.db import migrations

from django_migration_fixture import fixture
from apps import community


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(community, ['initial_data.json'])),

    ]
