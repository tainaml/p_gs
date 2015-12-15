# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='tag_order',
            field=models.IntegerField(default=0),
        ),
    ]
