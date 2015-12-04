# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.ForeignKey(to='configuration.ConfigKey', unique=True),
        ),
    ]
