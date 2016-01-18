# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0005_auto_20151112_0902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complainttype',
            options={'ordering': ['order']},
        ),
    ]
