# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20150928_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='taxonomies',
            field=models.ManyToManyField(related_name='feeds', to='taxonomy.Taxonomy'),
        ),
    ]
