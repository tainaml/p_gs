# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-01 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0012_auto_20160830_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='created_in',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created In'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='type',
            field=models.IntegerField(choices=[(1, 'Info'), (2, 'Danger'), (3, 'Warning'), (4, 'Success')]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='updated_in',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated In'),
        ),
    ]
