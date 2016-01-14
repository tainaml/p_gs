# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedobject',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 19, 6, 35, 396927, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
