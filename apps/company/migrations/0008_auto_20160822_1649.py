# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-22 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.CompanyContactType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='companycontacttype',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Description'),
        ),
    ]
