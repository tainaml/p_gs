# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_auto_20150908_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objecttaxonomy',
            name='taxonomy',
            field=models.ForeignKey(related_name='taxonomy_objects', to='taxonomy.Taxonomy'),
        ),
        migrations.AlterField(
            model_name='taxonomy',
            name='parent',
            field=models.ForeignKey(related_name='taxonomies', blank=True, to='taxonomy.Taxonomy', null=True),
        ),
        migrations.AlterField(
            model_name='taxonomy',
            name='term',
            field=models.ForeignKey(related_name='taxonomies', to='taxonomy.Term'),
        ),
    ]
