# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomy',
            name='parent',
            field=models.ForeignKey(blank=True, to='taxonomy.Taxonomy', null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='parent',
            field=models.ForeignKey(blank=True, to='taxonomy.Term', null=True),
        ),
    ]
