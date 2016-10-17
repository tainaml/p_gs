#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models.tags import Tags
from apps.taxonomy.models import Taxonomy
from apps.community.models import Community


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


    def __init__(self, *args, **kwargs):
        super(FeedObject, self).__init__(*args, **kwargs)

        self.official__old_value = self.official

    def __unicode__(self):
        if self.content_object and self.content_object.id:
            if self.content_type.model=="article" or self.content_type.model=="question":
                return ("[{0}] - ".format(self.content_type.model)).upper() + self.content_object.title

        return "No related object"