# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 18:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0027_auto_20161103_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': [('change_other_articles', 'Permiss\xe3o para editar artigos de outros autores')]},
        ),
    ]