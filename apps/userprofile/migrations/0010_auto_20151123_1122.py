# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_userprofile_contributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city_hometown',
            field=models.ForeignKey(related_name='profiles_city_hometown', blank=True, to='userprofile.City', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(related_name='profiles_city', blank=True, to='userprofile.City', null=True),
        ),
    ]
