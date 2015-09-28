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
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('abbreviation', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responsibility', models.CharField(max_length=60)),
                ('company', models.CharField(max_length=60)),
                ('date_begin', models.DateField(null=True, blank=True)),
                ('date_end', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('abbreviation', models.CharField(max_length=3)),
                ('country', models.ForeignKey(related_name='states', to='userprofile.Country')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=1, null=True, blank=True)),
                ('profile_picture', models.ImageField(default=b'', upload_to=b'userprofile/%Y/%m/%d', blank=True)),
                ('city', models.ForeignKey(blank=True, to='userprofile.City', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='occupation',
            name='profile',
            field=models.ForeignKey(to='userprofile.UserProfile'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(related_name='cities', to='userprofile.State'),
        ),
    ]
