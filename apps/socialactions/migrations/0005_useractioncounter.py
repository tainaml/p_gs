# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialactions', '0004_counter'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActionCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_type', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('author', models.ForeignKey(related_name='user_counter', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
