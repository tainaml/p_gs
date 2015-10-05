# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_auto_20151002_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wizard_step',
            field=models.IntegerField(default=0),
        ),
    ]
