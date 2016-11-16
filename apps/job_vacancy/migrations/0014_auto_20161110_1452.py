# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-10 17:52
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0013_auto_20161028_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobvacancylocation',
            name='cities',
            field=smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='state', chained_model_field='state', null=True, to='geography.City', verbose_name='Cidades'),
        ),
        migrations.AlterField(
            model_name='jobvacancylocation',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.State', verbose_name='Estados'),
        ),
    ]