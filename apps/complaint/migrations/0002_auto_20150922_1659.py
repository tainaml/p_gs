# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('complaint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='author',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 19, 59, 6, 438945, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
