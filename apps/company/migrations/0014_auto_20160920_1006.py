# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20160919_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='companycontacttype',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o'),
        ),
    ]