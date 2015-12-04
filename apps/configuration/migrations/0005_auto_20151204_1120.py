# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_configkey_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configkey',
            name='group',
            field=models.ForeignKey(related_name='config_keys', verbose_name='Configs Keys', to='configuration.ConfigGroup'),
        ),
    ]
