# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150825_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailvalidation',
            name='token_type',
            field=models.IntegerField(),
        ),
    ]
