# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='profile',
            field=models.ForeignKey(related_name='occupation', to='userprofile.UserProfile'),
        ),
    ]
