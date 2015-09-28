# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20150924_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='relevance',
        ),
    ]
