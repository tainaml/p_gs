# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20150828_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
