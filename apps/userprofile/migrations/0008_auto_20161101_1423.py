# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-01 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_responsibility_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsibility',
            old_name='text',
            new_name='about',
        ),
        migrations.AddField(
            model_name='responsibility',
            name='main_activity',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='responsibility',
            name='more_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='responsibility',
            name='study',
            field=models.TextField(blank=True, null=True),
        ),
    ]
