# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 21:37
from __future__ import unicode_literals

import apps.core.models.plataform
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20161205_1837'),
    ]

    operations = [

        migrations.AlterField(
            model_name='course',
            name='affiliate_link',
            field=models.URLField(verbose_name='Link afiliado'),
        ),
        migrations.AlterField(
            model_name='course',
            name='external_author',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Autor externo'),
        ),
        migrations.AlterField(
            model_name='course',
            name='internal_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='Autor interno'),
        ),
        migrations.AlterField(
            model_name='course',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='languages', to='core.Language', verbose_name='Linguagens'),
        ),
        migrations.AlterField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Avalia\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='course',
            name='related_courses',
            field=models.ManyToManyField(blank=True, related_name='_course_related_courses_+', to='core.Course', verbose_name='Cursos relacionados'),
        ),
        migrations.AlterField(
            model_name='course',
            name='taxonomies',
            field=models.ManyToManyField(blank=True, related_name='courses', to='taxonomy.Taxonomy', verbose_name='Taxonomia'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculums', to='core.Course', verbose_name='Curso'),
        ),
        migrations.AlterField(
            model_name='language',
            name='acronym',
            field=models.CharField(max_length=10, verbose_name='Sigla'),
        ),
        migrations.AddField(
            model_name='course',
            name='plataform',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='core.Plataform', verbose_name='Plataform'),
            preserve_default=False,
        ),
    ]
