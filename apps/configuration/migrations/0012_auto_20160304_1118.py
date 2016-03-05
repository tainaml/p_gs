# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0011_auto_20160224_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configkey',
            name='group',
            field=models.ForeignKey(related_name='config_keys', verbose_name='COnfigurar Chaves', to='configuration.ConfigGroup'),
        ),
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(related_name='config_values', verbose_name='Configurar Chaves', to='configuration.ConfigKey'),
        ),
    ]
