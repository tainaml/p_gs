# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150825_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailvalidation',
            name='token_type',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='mailvalidation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
