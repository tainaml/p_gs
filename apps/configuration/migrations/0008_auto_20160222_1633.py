# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_auto_20151209_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='configkey',
            name='show',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(related_name='config_values', verbose_name='Config Values', to='configuration.ConfigKey'),
        ),
    ]
