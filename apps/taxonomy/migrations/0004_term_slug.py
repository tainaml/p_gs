# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_auto_20151007_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='slug',
            field=models.SlugField(default=b'', blank=True),
        ),
    ]
