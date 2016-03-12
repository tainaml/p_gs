# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=60)),
                ('date_begin', models.DateField(null=True, blank=True)),
                ('date_end', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('text', ckeditor.fields.RichTextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=1, null=True, blank=True)),
                ('profile_picture', models.ImageField(default=b'', upload_to=b'userprofile/%Y/%m/%d', blank=True)),
                ('contributor', models.BooleanField(default=False)),
                ('wizard_step', models.IntegerField(default=0)),
                ('city', models.ForeignKey(related_name='profiles_city', blank=True, to='geography.City', null=True)),
                ('city_hometown', models.ForeignKey(related_name='profiles_city_hometown', blank=True, to='geography.City', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='occupation',
            name='profile',
            field=models.ForeignKey(related_name='occupation', to='userprofile.UserProfile'),
        ),
        migrations.AddField(
            model_name='occupation',
            name='responsibility',
            field=models.ForeignKey(to='userprofile.Responsibility'),
        ),
    ]
