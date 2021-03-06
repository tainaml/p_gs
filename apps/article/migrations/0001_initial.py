# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 19:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(default=b'', max_length=150)),
                ('text', models.TextField(max_length=100000)),
                ('image', models.ImageField(blank=True, default=b'', upload_to=b'article/%Y/%m/%d')),
                ('createdin', models.DateTimeField(auto_now_add=True)),
                ('updatein', models.DateTimeField(auto_now=True)),
                ('publishin', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(3, 'Rascunho'), (2, 'Lixo'), (4, 'Publicado')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
        ),
    ]
