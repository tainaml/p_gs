# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailvalidation',
            name='link_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 20, 21, 40, 758548)),
        ),
    ]
