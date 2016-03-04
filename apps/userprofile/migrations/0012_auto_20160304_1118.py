# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20160121_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default=b'', null=True, upload_to=b'userprofile/%Y/%m/%d', blank=True),
        ),
    ]
