# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 19:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taxonomy', '0001_initial'),
        ('geography', '0001_initial'),
        ('certification', '0001_initial'),
        ('userprofile', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='Exigency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='JobRegime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='T\xedtulo')),
                ('slug', models.SlugField(default='', max_length=150, verbose_name='Slug')),
                ('job_vacancy_date', models.DateField(default=django.utils.timezone.now, verbose_name='Data')),
                ('description', models.TextField(max_length=10000, verbose_name='Descri\xe7\xe3o')),
                ('job_vacancy_responsibility', models.TextField(max_length=10000, null=True, verbose_name='Descri\xe7ao da resposabilidade')),
                ('home_office', models.BooleanField(verbose_name='Home Office')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Quantidade')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='N\xfamero de Telefone')),
                ('site', models.CharField(blank=True, max_length=100, null=True, verbose_name='Web Site')),
                ('contact', models.TextField(blank=True, max_length=10000, null=True, verbose_name='Contato')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certification.Certification', verbose_name='Certifica\xe7\xe3o')),
                ('exigency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exigency')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cities', smart_selects.db_fields.ChainedManyToManyField(chained_field='state', chained_model_field='state', to='geography.City', verbose_name='Cidades')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.Country', verbose_name='Pa\xeds')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyResponsibilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exigency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exigency')),
                ('experience', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Experience', verbose_name='Experi\xeancia')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Taxonomy', verbose_name='Item')),
            ],
        ),
        migrations.CreateModel(
            name='SalaryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLoad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyResponsibility',
            fields=[
                ('job_vacancy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='resposibility', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho')),
                ('responsibility', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Responsibility', verbose_name='\xc1rea de atua\xe7\xe3o')),
                ('responsibility_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.JobVacancyResponsibilityType', verbose_name='tipo da \xe1rea de atua\xe7\xe3o')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('fixed_value', models.FloatField(blank=True, null=True, verbose_name='Valor fixo')),
                ('range_value_from', models.FloatField(blank=True, null=True, verbose_name='Intervalo de')),
                ('range_value_to', models.FloatField(blank=True, null=True, verbose_name='Intervalo para')),
                ('job_vacancy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='salary', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho')),
                ('regime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.SalaryType', verbose_name='Tipo de sal\xe1rio')),
            ],
        ),
        migrations.AddField(
            model_name='requirement',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Level', verbose_name='N\xedvel'),
        ),
        migrations.AddField(
            model_name='jobvacancylocation',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AddField(
            model_name='jobvacancylocation',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='country', on_delete=django.db.models.deletion.CASCADE, to='geography.State', verbose_name='Estados'),
        ),
        migrations.AddField(
            model_name='jobvacancycertification',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='job_vacancy.JobVacancy', verbose_name='Vaga de trabalho'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='benefits',
            field=models.ManyToManyField(blank=True, to='job_vacancy.Benefit', verbose_name='Benef\xedcios'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to='company.Company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='regime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.JobRegime', verbose_name='Regime'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='workload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.WorkLoad', verbose_name='Carga hor\xe1ria'),
        ),
    ]
