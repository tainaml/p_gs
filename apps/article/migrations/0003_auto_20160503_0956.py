# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160414_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(3, 'Rascunho'), (2, 'Lixo'), (4, 'Publicado')]),
        ),
    ]
