# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_responsibility_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsibility',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Sobre'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='active',
            field=models.BooleanField(default=False, verbose_name='A\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='categories',
            field=models.ManyToManyField(related_name='responsibilities', to='taxonomy.Taxonomy', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='main_activity',
            field=models.TextField(blank=True, null=True, verbose_name='Main Activities'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='more_info',
            field=models.TextField(blank=True, null=True, verbose_name='More info'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='name',
            field=models.CharField(max_length=60, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='responsibility',
            name='study',
            field=models.TextField(blank=True, null=True, verbose_name='What study'),
        ),
    ]
