# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.ForeignKey(related_name='cities', to='userprofile.State'),
        ),
        migrations.AlterField(
            model_name='state',
            name='country',
            field=models.ForeignKey(related_name='states', to='userprofile.Country'),
        ),
    ]
