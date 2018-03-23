#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from apps.core.models.tags import Tags
from apps.taxonomy.models import Taxonomy
from apps.community.models import Community
from django.utils.translation import ugettext as _
from django.utils import timezone


class FeedObject(models.Model):

    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)
    date = models.DateTimeField(null=True, auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    taxonomies = models.ManyToManyField(Taxonomy, related_name='feeds', null=True, blank=True)
    communities = models.ManyToManyField(Community, related_name='feeds', null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='feeds', null=True, blank=True)

    official = models.BooleanField(null=False, blank=False, default=False)

    # SEO
    seo_no_index = models.BooleanField(default=False)
    seo_no_follow = models.BooleanField(default=False)

    @property
    def title(self):
        return self.content_object.title

    @property
    def image(self):
        return self.content_object.image if hasattr(self.content_object, "image") else None

    @property
    def author_full_name(self):
        return self.content_object.author.get_full_name()




    def __init__(self, *args, **kwargs):
        super(FeedObject, self).__init__(*args, **kwargs)

        self.official__old_value = self.official

    def __unicode__(self):
        if self.content_object and self.content_object.id:
            if self.content_type.model=="article" or self.content_type.model=="question":
                return ("[{0}] - ".format(self.content_type.model)).upper() + self.content_object.title

        return "No related object"

class ProfileStatus(models.Model):

    text = models.TextField(null=False, max_length=256)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='profile_status', verbose_name=_('Author'))
    VECTOR = SearchVector("profile_status__text", weight="B")
    updatein = models.DateTimeField(null=False, auto_now=True)
    publishin = models.DateTimeField(null=True, db_index=True, default=timezone.now)
    status = models.BooleanField(default=True)
    feed = GenericRelation(FeedObject, related_name="profile_status", related_query_name="profile_status")

    search_vector = SearchVectorField(null=True)

    comment_count = models.PositiveIntegerField(null=True, blank=True)
    like_count = models.PositiveIntegerField(null=True, blank=True)
    dislike_count = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        feed_id =  self.feed.get().id
        username = self.author.username
        return reverse('profile:profilestatus', args=[username, feed_id])

    def can_delete(self, user):
        return self.author == user

    @cached_property
    def title(self):
        return self.text
