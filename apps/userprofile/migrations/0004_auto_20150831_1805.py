# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20150828_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupation',
            name='user',
        ),
        migrations.AddField(
            model_name='occupation',
            name='profile',
            field=models.ForeignKey(to='userprofile.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
    ]
