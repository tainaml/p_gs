# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20160223_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=25000),
        ),
    ]
