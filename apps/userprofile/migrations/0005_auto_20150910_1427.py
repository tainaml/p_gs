# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20150831_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupation',
            name='description',
        ),
        migrations.AddField(
            model_name='occupation',
            name='company',
            field=models.CharField(default='lorem ipsum', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='occupation',
            name='date_begin',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='occupation',
            name='date_end',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='occupation',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
