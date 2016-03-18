# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 16:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0007_auto_20160317_1526'),
        ('taxonomy', '0002_auto_20160317_1526'),
        ('certification', '0001_initial'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Exigency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='JobRegime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(default='', max_length=150, verbose_name='Slug')),
                ('job_vacancy_date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('description', models.TextField(max_length=10000, verbose_name='Description')),
                ('job_vacancy_responsibility', models.TextField(max_length=10000, null=True, verbose_name='Responsibility Description')),
                ('home_office', models.BooleanField(verbose_name='Home Office')),
                ('quantity', models.PositiveIntegerField(null=True, verbose_name='Quantity')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone Number')),
                ('site', models.CharField(blank=True, max_length=100, null=True, verbose_name='Web Site')),
                ('contact', models.TextField(max_length=10000, null=True, verbose_name='Contato')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certification.Certification', verbose_name='Certification')),
                ('exigency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exigency')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyResponsibilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exigency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Exigency', verbose_name='Exigency')),
                ('experience', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Experience', verbose_name='Experience')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Taxonomy', verbose_name='Item')),
            ],
        ),
        migrations.CreateModel(
            name='SalaryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLoad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='JobVacancyResponsibility',
            fields=[
                ('job_vacancy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='resposibility', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Job Vacancy')),
                ('responsibility', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Responsibility', verbose_name='Responsibility')),
                ('responsibility_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.JobVacancyResponsibilityType', verbose_name='Responsibility Type')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('fixed_value', models.FloatField(blank=True, null=True, verbose_name='Fixed value')),
                ('range_value_from', models.FloatField(blank=True, null=True, verbose_name='Range from')),
                ('range_value_to', models.FloatField(blank=True, null=True, verbose_name='Range to')),
                ('job_vacancy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='salary', serialize=False, to='job_vacancy.JobVacancy', verbose_name='Job Vacancy')),
                ('regime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.SalaryType', verbose_name='Salary Type')),
            ],
        ),
        migrations.AddField(
            model_name='requirement',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='job_vacancy.JobVacancy', verbose_name='Job Vacancy'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.Level', verbose_name='N\xedvel'),
        ),
        migrations.AddField(
            model_name='jobvacancycertification',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='job_vacancy.JobVacancy', verbose_name='Job Vacancy'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='benefits',
            field=models.ManyToManyField(to='job_vacancy.Benefit', verbose_name='Benefits'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='cities',
            field=models.ManyToManyField(to='geography.City', verbose_name='Cidades'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_vacancys', to='company.Company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='regime',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.JobRegime', verbose_name='Regime'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='states',
            field=models.ManyToManyField(to='geography.State', verbose_name='Cidades'),
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='workload',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job_vacancy.WorkLoad', verbose_name='Work Load'),
        ),
    ]
