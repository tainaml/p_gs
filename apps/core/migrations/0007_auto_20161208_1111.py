# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 14:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20161208_1111'),
        ('core', '0006_companyuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyUser',
        ),
        migrations.CreateModel(
            name='CompanyProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('company.company',),
        ),
    ]
