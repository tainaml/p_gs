# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-09 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyContactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.AddField(
            model_name='companycontact',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.CompanyContactType', verbose_name='Tipo'),
        ),
    ]