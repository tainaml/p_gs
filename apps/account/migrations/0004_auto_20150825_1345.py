# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150825_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailvalidation',
            name='link_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 25, 13, 45, 18, 36907)),
        ),
    ]
