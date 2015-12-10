# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20150930_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(3, 'Draft'), (2, 'Trash'), (4, 'Publish')]),
        ),
    ]
