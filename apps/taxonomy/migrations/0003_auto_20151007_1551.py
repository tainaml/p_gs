# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomy',
            name='parent',
            field=models.ForeignKey(related_name='taxonomies_children', blank=True, to='taxonomy.Taxonomy', null=True),
        ),
    ]
