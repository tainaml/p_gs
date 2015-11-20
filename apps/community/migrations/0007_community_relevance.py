# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_auto_20150929_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='relevance',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
        ),
    ]
