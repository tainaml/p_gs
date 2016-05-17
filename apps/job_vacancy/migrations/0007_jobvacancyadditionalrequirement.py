# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-17 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0006_remove_jobvacancy_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobVacancyAdditionalRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512, verbose_name='Aditional Requirement')),
                ('job_vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_requirements', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho')),
            ],
        ),
    ]
