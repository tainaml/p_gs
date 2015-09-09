# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20150908_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='question_owner', default=1, to='question.Question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.OneToOneField(related_name='correct_answer', null=True, blank=True, to='question.Answer'),
        ),
    ]
