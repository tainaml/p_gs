# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20151204_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(to='configuration.ConfigKey'),
        )
    ]
