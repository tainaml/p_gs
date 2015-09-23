# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_object_id', models.PositiveIntegerField()),
                ('notification_date', models.DateTimeField(auto_now=True)),
                ('notification_action', models.PositiveIntegerField()),
                ('author', models.ForeignKey(related_name='notifications_sent', to=settings.AUTH_USER_MODEL)),
                ('target_content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('to', models.ForeignKey(related_name='notifications_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
