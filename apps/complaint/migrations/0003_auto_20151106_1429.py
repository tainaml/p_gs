# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0002_complaint_communities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='communities',
            field=models.ManyToManyField(to='community.Community', null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
    ]
