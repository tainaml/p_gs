# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_feedobject_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedobject',
            name='official',
            field=models.BooleanField(default=False),
        ),
    ]
