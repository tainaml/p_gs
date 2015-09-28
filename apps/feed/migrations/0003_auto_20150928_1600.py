# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_feedobject_taxonomies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='taxonomies',
            field=models.ManyToManyField(related_name='feeds', to='taxonomy.Taxonomy'),
        ),
    ]
