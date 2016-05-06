# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 19:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_vacancy', '0002_auto_20160414_1905'),
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
            name='benefits',
            field=models.ManyToManyField(blank=True, to='job_vacancy.Benefit', verbose_name='Benef\xedcios'),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Descri\xe7\xe3o'),
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
            model_name='jobvacancycertification',
            name='certification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certification.Certification', verbose_name='Certifica\xe7\xe3o'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exigency'),
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
            model_name='requirement',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Level', verbose_name='N\xedvel'),
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
