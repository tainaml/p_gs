# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0004_term_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonomy',
            name='slug',
            field=models.SlugField(default=b'', blank=True),
        ),
    ]
