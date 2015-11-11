# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_auto_20150929_1135'),
        ('complaint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='communities',
            field=models.ManyToManyField(to='community.Community'),
        ),
    ]
