# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=512)),
                ('object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='complaint_type',
            field=models.ForeignKey(to='complaint.ComplaintType'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
    ]
