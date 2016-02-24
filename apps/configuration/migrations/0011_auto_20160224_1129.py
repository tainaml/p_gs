# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configkey',
            name='group',
            field=models.ForeignKey(related_name='config_keys', verbose_name='Configs Keys', to='configuration.ConfigGroup'),
        ),
    ]
