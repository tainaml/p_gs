# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_auto_20150929_1135'),
        ('feed', '0003_auto_20150930_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedobject',
            name='communities',
            field=models.ManyToManyField(related_name='feeds', to='community.Community'),
        ),
    ]
