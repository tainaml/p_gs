# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20151002_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupation',
            name='responsibility',
            field=models.ForeignKey(to='userprofile.Responsibility'),
            preserve_default=False,
        ),
    ]
