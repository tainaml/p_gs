# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-09 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0016_merge_20161209_1418'),
    ]

    operations = [
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
            name='study',
            field=models.TextField(blank=True, null=True, verbose_name='What study'),
        ),
    ]