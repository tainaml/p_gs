# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_relevance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='relevance',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
        ),
    ]
