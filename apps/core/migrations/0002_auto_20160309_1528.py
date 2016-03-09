# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.operations import UnaccentExtension

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        UnaccentExtension()
    ]
