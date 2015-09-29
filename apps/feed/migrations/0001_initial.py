# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relevance', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('taxonomies', models.ManyToManyField(related_name='feeds', to='taxonomy.Taxonomy')),
            ],
        ),
    ]
