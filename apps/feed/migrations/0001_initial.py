# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
        ('community', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relevance', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('official', models.BooleanField(default=False)),
                ('communities', models.ManyToManyField(related_name='feeds', to='community.Community')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('tags', models.ManyToManyField(related_name='feeds', to='core.Tags')),
                ('taxonomies', models.ManyToManyField(related_name='feeds', to='taxonomy.Taxonomy')),
            ],
        ),
    ]
