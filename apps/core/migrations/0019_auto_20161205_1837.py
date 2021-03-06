# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 21:37
from __future__ import unicode_literals
from django.db import migrations, models
from django.db import migrations
from apps.core.models.plataform import plataform_image_upload


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_curriculum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plataform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('description', models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o')),
                ('image', models.ImageField(blank=True, upload_to=plataform_image_upload)),
            ],
        ),
    ]
