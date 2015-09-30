# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_feedobject_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedobject',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
