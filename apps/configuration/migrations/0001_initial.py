# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ConfigKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('show', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=None, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_keys', to='configuration.ConfigGroup', verbose_name='COnfigurar Chaves')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_values', to='configuration.ConfigKey', verbose_name='Configurar Chaves')),
            ],
        ),
    ]
