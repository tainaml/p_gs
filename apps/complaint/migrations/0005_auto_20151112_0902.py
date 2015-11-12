# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0004_complainttype_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='communities',
            field=models.ManyToManyField(to='community.Community'),
        ),
    ]
