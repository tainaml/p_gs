# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 16:53
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_auto_20160920_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='vector_title_text',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
