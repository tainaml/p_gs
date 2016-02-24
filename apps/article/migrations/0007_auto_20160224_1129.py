# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20160223_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(related_name='articles', verbose_name='Author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(3, 'Draft'), (2, 'Trash'), (4, 'Publish')]),
        ),
    ]
