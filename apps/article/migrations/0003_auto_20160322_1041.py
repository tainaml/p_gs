# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 13:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160317_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(3, 'Rascunho'), (2, 'Lixo'), (4, 'Publicado')]),
        ),
    ]