# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-16 12:54
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_profilestatus_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilestatus',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]