# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=2048),
        ),
    ]
