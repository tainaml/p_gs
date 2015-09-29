# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(related_name='taxonomies', blank=True, to='taxonomy.Taxonomy', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, to='taxonomy.Term', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='taxonomy',
            name='term',
            field=models.ForeignKey(related_name='taxonomies', to='taxonomy.Term'),
        ),
    ]
