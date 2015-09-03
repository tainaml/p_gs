# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 27, 21, 38, 22, 423521, tzinfo=utc)),
        ),
    ]
