#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models import Community


def get_community_by_params(params={}, order_by=[], limit=None, offset=None):
    try:
        community = Community.objects.filter(**params).order_by(*order_by)[offset:limit]
    except Community.DoesNotExist:
        return False

    return community


def get_community(slug=None):
    try:
        community = Community.objects.get(slug=slug)
    except Community.DoesNotExist:
        return None

    return community


def get_category_communities(taxonomies_id=None):
    try:
        communities = Community.objects.filter(taxonomy__in=taxonomies_id, taxonomy__term__slug='categoria')
    except Community.DoesNotExist:
        return None

    return communities

def get_all_communities(criteria='', items_per_page=10, page=1):

    if items_per_page > 100:
        items_per_page = 100

    queryset = Community.objects.filter(title__icontains=criteria).only("slug", "title")

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1
    communities = []
    if items_per_page and page:
        communities = Paginator(queryset, items_per_page)
        try:
            communities = communities.page(page)
        except PageNotAnInteger:
            communities = communities.page(1)
        except EmptyPage:
            communities = []


    return [{'slug': community.slug, 'title': community.title} for community in communities]