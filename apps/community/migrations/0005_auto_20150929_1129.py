# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20150929_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='taxonomy',
            field=models.OneToOneField(related_name='community_related', db_constraint=b'community_taxonomy_contraint', to='taxonomy.Taxonomy'),
        ),
    ]
