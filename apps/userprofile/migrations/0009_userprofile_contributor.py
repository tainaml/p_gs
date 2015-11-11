# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_userprofile_wizard_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='contributor',
            field=models.BooleanField(default=False),
        ),
    ]
