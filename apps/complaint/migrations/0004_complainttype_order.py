# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0003_auto_20151106_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='complainttype',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
