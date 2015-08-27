# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20150827_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(default=b'', unique=True, max_length=2048),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default=b'', unique=True, max_length=100),
        ),
    ]
