# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-15 19:34
from __future__ import unicode_literals

import apps.core.models.course
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20161214_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='affiliate_link',
            field=models.URLField(blank=True, null=True, verbose_name='Affiliate link'),
        ),
        migrations.AlterField(
            model_name='course',
            name='class_link',
            field=models.URLField(blank=True, null=True, verbose_name='Class Link'),
        ),
        migrations.AlterField(
            model_name='course',
            name='external_author',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='External Author'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, upload_to=apps.core.models.course.course_image_upload, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='course',
            name='internal_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='Internal author'),
        ),
        migrations.AlterField(
            model_name='course',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='languages', to='core.Language', verbose_name='Languages'),
        ),
        migrations.AlterField(
            model_name='course',
            name='plataform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='core.Plataform', verbose_name='Plataform'),
        ),
        migrations.AlterField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='course',
            name='related_courses',
            field=models.ManyToManyField(blank=True, related_name='_course_related_courses_+', to='core.Course', verbose_name='Related Courses'),
        ),
        migrations.AlterField(
            model_name='course',
            name='taxonomies',
            field=models.ManyToManyField(blank=True, related_name='courses', to='taxonomy.Taxonomy', verbose_name='Taxonomy'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculums', to='core.Course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='language',
            name='acronym',
            field=models.CharField(max_length=10, verbose_name='Acronym'),
        ),
    ]
