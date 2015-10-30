# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('text', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='occupation',
            name='responsibility',
        ),
    ]
