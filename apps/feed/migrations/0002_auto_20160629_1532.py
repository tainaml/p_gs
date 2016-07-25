# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-29 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='communities',
            field=models.ManyToManyField(blank=True, null=True, related_name='feeds', to='community.Community'),
        ),
        migrations.AlterField(
            model_name='feedobject',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='feeds', to='core.Tags'),
        ),
        migrations.AlterField(
            model_name='feedobject',
            name='taxonomies',
            field=models.ManyToManyField(blank=True, null=True, related_name='feeds', to='taxonomy.Taxonomy'),
        ),
    ]
