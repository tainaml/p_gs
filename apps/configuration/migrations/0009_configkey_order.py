# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0008_auto_20160222_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='configkey',
            name='order',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
