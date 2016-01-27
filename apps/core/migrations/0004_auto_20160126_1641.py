# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tags_tag_order'),
    ]

    operations = [
        UnaccentExtension()
    ]
