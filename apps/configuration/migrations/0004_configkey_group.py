# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_auto_20151204_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='configkey',
            name='group',
            field=models.ForeignKey(default=1, to='configuration.ConfigGroup'),
            preserve_default=False,
        ),
    ]
