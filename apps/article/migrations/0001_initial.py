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
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('createdin', models.DateTimeField(auto_now_add=True)),
                ('updatein', models.DateTimeField(auto_now=True)),
                ('publishin', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(0, b'Draft'), (2, b'Trash'), (4, b'Publish')])),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
