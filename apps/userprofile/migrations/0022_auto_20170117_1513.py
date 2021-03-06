# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-17 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0021_merge_20170117_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsibility',
            name='categories',
            field=models.ManyToManyField(related_name='responsibilities', to='taxonomy.Taxonomy', verbose_name='Categorias'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='main_activity',
            field=models.TextField(blank=True, null=True, verbose_name='Principais atividades'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='more_info',
            field=models.TextField(blank=True, null=True, verbose_name='Mais informa\xe7\xf5es'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='study',
            field=models.TextField(blank=True, null=True, verbose_name='O que estudar'),
        ),
    ]
