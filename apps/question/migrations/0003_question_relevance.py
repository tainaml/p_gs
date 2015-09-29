# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='relevance',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
        ),
    ]
