# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialactions', '0002_auto_20150928_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraction',
            name='target_user',
            field=models.ForeignKey(related_name='target_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
