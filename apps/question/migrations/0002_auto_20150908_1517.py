# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.OneToOneField(null=True, blank=True, to='question.Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
