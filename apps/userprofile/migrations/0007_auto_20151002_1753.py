# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_occupation_responsibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsibility',
            name='text',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
    ]
