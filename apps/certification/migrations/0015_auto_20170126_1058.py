# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-26 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_taxonomy_update_in'),
        ('certification', '0014_merge_20160922_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Sobre'),
        ),
        migrations.AddField(
            model_name='certification',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='certification',
            name='more_info',
            field=models.TextField(blank=True, null=True, verbose_name='Mais informa\xe7\xf5es'),
        ),
        migrations.AddField(
            model_name='certification',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='certification',
            name='taxonomies',
            field=models.ManyToManyField(related_name='certifications', to='taxonomy.Taxonomy', verbose_name='Related with'),
        ),
        migrations.AddField(
            model_name='certification',
            name='where_get',
            field=models.TextField(blank=True, null=True, verbose_name='O que estudar'),
        ),
    ]
