# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20161103_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': [('change_other_questions', 'Permiss\xe3o para editar perguntas de outros autores')]},
        ),
    ]