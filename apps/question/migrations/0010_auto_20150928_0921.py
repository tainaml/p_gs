# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_auto_20150925_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='publish_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='relevance',
        ),
    ]
