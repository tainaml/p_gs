# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150824_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailvalidation',
            old_name='is_active',
            new_name='active',
        ),
        migrations.AlterField(
            model_name='mailvalidation',
            name='link_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 25, 13, 44, 22, 782700)),
        ),
    ]
