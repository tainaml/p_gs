# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20150910_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupation',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
