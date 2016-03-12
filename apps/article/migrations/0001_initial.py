# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(default=b'', max_length=150)),
                ('text', ckeditor.fields.RichTextField(max_length=100000)),
                ('image', models.ImageField(default=b'', upload_to=b'article/%Y/%m/%d', blank=True)),
                ('createdin', models.DateTimeField(auto_now_add=True)),
                ('updatein', models.DateTimeField(auto_now=True)),
                ('publishin', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(3, 'Rascunho'), (2, 'Lixo'), (4, 'Publicar')])),
                ('author', models.ForeignKey(related_name='articles', verbose_name='Autor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
