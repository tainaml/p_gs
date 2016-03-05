# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20160114_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=25000),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
