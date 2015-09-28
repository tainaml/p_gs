# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_question_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 14, 50, 48, 116136, tzinfo=utc)),
        ),
    ]
