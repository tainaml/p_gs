# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-30 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20160830_1338'),
        ('temp_comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempcomment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article'),
        ),
    ]