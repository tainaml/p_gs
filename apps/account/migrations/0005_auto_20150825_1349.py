# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150825_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailvalidation',
            name='link_date',
            field=models.DateTimeField(),
        ),
    ]
