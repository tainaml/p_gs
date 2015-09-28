# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django_migration_fixture import fixture
from apps import community

class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20150928_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=150)),
                ('description', models.TextField(max_length=2048)),
                ('image', models.ImageField(default=b'', upload_to=b'community/%Y/%m/%d', blank=True)),
                ('taxonomy', models.ForeignKey(to='taxonomy.Taxonomy')),
            ],
        ),

        migrations.RunPython(**fixture(community, ['initial_data.json'])),


    ]
