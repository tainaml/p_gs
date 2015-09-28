# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20150924_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='relevance',
        ),
    ]
