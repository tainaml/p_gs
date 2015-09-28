# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20150928_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='taxonomies',
            field=models.ManyToManyField(related_query_name=b'feeds', related_name='feeds', to='taxonomy.Taxonomy'),
        ),
    ]
