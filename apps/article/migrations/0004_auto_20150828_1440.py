# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0003_auto_20150827_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='autor',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(related_name='articles', default='', verbose_name='Author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=b'', unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
