# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='profile',
            field=models.ForeignKey(related_name='occupation', to='userprofile.UserProfile'),
        ),
    ]
