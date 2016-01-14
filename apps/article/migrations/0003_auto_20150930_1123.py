# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=2048),
        ),
    ]
