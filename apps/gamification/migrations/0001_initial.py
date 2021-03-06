# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-26 18:03
from __future__ import unicode_literals

import apps.gamification.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0018_auto_20171003_1134'),
        ('geography', '0003_auto_20160606_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(verbose_name='Value')),
                ('communitiy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='community.Community', verbose_name='Community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_ranks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='XPTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.PositiveIntegerField(choices=[(1, 'Credit'), (2, 'Debit')], validators=[apps.gamification.models.limit_transaction_types], verbose_name='Transaction Type')),
                ('action_type', models.PositiveIntegerField(choices=[(b'like', 1), (b'unlike', 2), (b'follow', 3), (b'favourite', 4), (b'suggest', 5), (b'comment', 6), (b'see-later', 7), (b'answer', 8)], validators=[apps.gamification.models.limit_actions], verbose_name='Action type')),
                ('value', models.PositiveIntegerField(verbose_name='Value')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_related', to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='geography.City')),
                ('communitiy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='community.Community', verbose_name='Community')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
