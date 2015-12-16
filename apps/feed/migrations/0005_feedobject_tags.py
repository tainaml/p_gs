# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tags'),
        ('feed', '0004_feedobject_communities'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedobject',
            name='tags',
            field=models.ManyToManyField(related_name='feeds', to='core.Tags'),
        ),
    ]
