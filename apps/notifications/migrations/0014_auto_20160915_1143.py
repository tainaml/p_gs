# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-15 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0013_auto_20160901_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='created_in',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='type',
            field=models.IntegerField(choices=[(1, 'Info'), (2, 'Perigo'), (3, 'Aviso'), (4, 'Sucesso')]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='updated_in',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
