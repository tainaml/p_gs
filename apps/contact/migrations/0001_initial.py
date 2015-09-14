# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_email', models.CharField(max_length=100, null=True, blank=True)),
                ('message', models.CharField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.ForeignKey(to='contact.ContactSubject'),
        ),
    ]
