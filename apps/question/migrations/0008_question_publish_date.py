# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20150924_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 14, 41, 16, 614933, tzinfo=utc)),
        ),
    ]
