
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20150922_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='relevance',
            field=models.DecimalField(default=0.0, max_digits=2, decimal_places=2),
        ),
    ]
