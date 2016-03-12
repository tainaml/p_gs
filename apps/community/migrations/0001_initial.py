# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
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
                ('relevance', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('taxonomy', models.OneToOneField(related_name='community_related', to='taxonomy.Taxonomy')),
            ],
        ),
    ]
