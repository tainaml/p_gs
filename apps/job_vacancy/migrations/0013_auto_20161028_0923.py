# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 12:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0012_auto_20160629_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='exigency',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='jobregime',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='benefits',
            field=models.ManyToManyField(blank=True, to='job_vacancy.Benefit', verbose_name='Benef\xedcios'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to='company.Company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='contact',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='Contato'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Est\xe1 ativo'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='job_vacancy_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='job_vacancy_responsibility',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='Descri\xe7ao da resposabilidade'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='phone_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='N\xfamero de Telefone'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='title',
            field=models.CharField(max_length=100, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='workload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.WorkLoad', verbose_name='Carga hor\xe1ria'),
        ),
        migrations.AlterField(
            model_name='jobvacancyadditionalrequirement',
            name='description',
            field=models.CharField(max_length=512, verbose_name='Requisito adicional'),
        ),
        migrations.AlterField(
            model_name='jobvacancyadditionalrequirement',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_requirements', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='jobvacancycertification',
            name='certification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certification.Certification', verbose_name='Certifica\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='jobvacancycertification',
            name='exigency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exig\xeancia'),
        ),
        migrations.AlterField(
            model_name='jobvacancycertification',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='jobvacancylocation',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='jobvacancyresponsibility',
            name='job_vacancy',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='resposibility', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='jobvacancyresponsibility',
            name='responsibility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Responsibility', verbose_name='\xc1rea de atua\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='jobvacancyresponsibility',
            name='responsibility_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.JobVacancyResponsibilityType', verbose_name='tipo da \xe1rea de atua\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='jobvacancyresponsibilitytype',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='level',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='exigency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exig\xeancia'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Experience', verbose_name='Experi\xeancia'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='fixed_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Valor fixo'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='job_vacancy',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='salary', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='range_value_from',
            field=models.FloatField(blank=True, null=True, verbose_name='Intervalo de'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='range_value_to',
            field=models.FloatField(blank=True, null=True, verbose_name='Intervalo para'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='regime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.SalaryType', verbose_name='Tipo de sal\xe1rio'),
        ),
        migrations.AlterField(
            model_name='salarytype',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='workload',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o'),
        ),
    ]