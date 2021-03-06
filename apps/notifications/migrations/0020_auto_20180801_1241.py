# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-01 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0019_auto_20180202_1514'),
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
