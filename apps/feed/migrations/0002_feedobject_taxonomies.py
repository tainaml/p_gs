# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20150928_1445'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedobject',
            name='taxonomies',
            field=models.ManyToManyField(to='taxonomy.Taxonomy'),
        ),
    ]
