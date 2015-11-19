# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialactions', '0003_useraction_target_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_type', models.PositiveIntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('target_user', models.ForeignKey(related_name='target_user_counter', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
