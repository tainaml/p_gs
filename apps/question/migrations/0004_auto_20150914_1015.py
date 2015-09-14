# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20150909_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='description',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(max_length=2048),
        ),
    ]
