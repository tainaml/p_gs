# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ConfigKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('show', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=None, null=True)),
                ('group', models.ForeignKey(related_name='config_keys', verbose_name='COnfigurar Chaves', to='configuration.ConfigGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigValues',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('key', models.ForeignKey(related_name='config_values', verbose_name='Configurar Chaves', to='configuration.ConfigKey')),
            ],
        ),
    ]
