# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_auto_20151123_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='state',
        ),
        migrations.RemoveField(
            model_name='state',
            name='country',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(related_name='profiles_city', blank=True, to='geography.City', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city_hometown',
            field=models.ForeignKey(related_name='profiles_city_hometown', blank=True, to='geography.City', null=True),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
