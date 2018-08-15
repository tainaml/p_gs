# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-01 15:41
from __future__ import unicode_literals

import apps.company.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0029_auto_20180202_1514'),
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
            model_name='company',
            name='taxonomies',
            field=models.ManyToManyField(related_name='companies', to='taxonomy.Taxonomy', verbose_name='Taxonomies'),
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
        migrations.AlterField(
            model_name='membership',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='permission',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Collaborator')], validators=[apps.company.models.limit_to_membershiptypes], verbose_name='Permission'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio'),
        ),
    ]
