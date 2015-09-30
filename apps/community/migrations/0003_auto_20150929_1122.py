# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='taxonomy',
            field=models.OneToOneField(related_name='community', to='taxonomy.Taxonomy'),
        ),
    ]
