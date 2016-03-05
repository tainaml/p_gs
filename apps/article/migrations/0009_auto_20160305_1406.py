# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20160304_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=100000),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
