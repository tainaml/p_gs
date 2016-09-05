#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe

__author__ = 'phillip'

from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
import re
from django_thumbor import generate_url
from django_user_agents.utils import get_user_agent

register = template.Library()

class NotValidURI(Exception):
    pass

class SiteUrlNotFound(Exception):
    pass

class URI():
    uri_regex = re.compile(r'((?P<scheme>\w+)://)?(?P<domain>[\w.-]+)?(:(?P<port>\d+))?(?P<path>[/[\w-]*(.(?P<content_type>[\w-]+))*)$')

    def __init__(self, uriparam=None):


        self.uri =  self.uri_regex.match(uriparam)

        if not self.uri:
            raise NotValidURI("String is not a valid uri %s" % uriparam)

        self.scheme = self.uri.group("scheme")
        self.domain = self.uri.group("domain")
        self.port = self.uri.group("port")
        self.path = self.uri.group("path")

    @property
    def absolute_uri(self):
        absolute_uri = ""
        absolute_uri+=self.scheme
        absolute_uri+="://"
        absolute_uri+=self.domain

        if self.port:
            absolute_uri+=":"
            absolute_uri+=self.port
        if self.path:
            absolute_uri+=self.path

        return absolute_uri

    def __unicode__(self):
        return self.absolute_uri


@register.filter
def absolute(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")
    return URI(value).absolute_uri


@register.filter
@stringfilter
def scheme(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")


    return URI(settings.SITE_URL+value).scheme

@register.filter
@stringfilter
def port(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")
    return URI(settings.SITE_URL+value).port


@register.filter
@stringfilter
def path(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")
    return URI(settings.SITE_URL+value).path

@register.filter
@stringfilter
def root(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")

    return URI(settings.SITE_URL).absolute_uri

regex_pattern_with_style = re.compile(u'src="(?P<url>/media/uploads/editor-uploads/.*?)".*?height:(?P<height>\d+)px.*?width:(?P<width>\d+)px"')
regex_pattern_with_attribute = re.compile(u'height="(?P<height>\d+)" src="(?P<url>/media/uploads/editor-uploads/.*?)".*?width="(?P<width>\d+)"')


def reduce_dimension(bigger, bigger_to, pair):
    return (bigger_to*pair)/bigger


def reduce_proportionally(width, height, is_mobile):
    max_width = settings.MAXIMUM_MOBILE_IMAGE_WIDTH if is_mobile else settings.MAXIMUM_PC_IMAGE_WIDTH
    max_height = settings.MAXIMUM_MOBILE_IMAGE_WIDTH if is_mobile else settings.MAXIMUM_PC_IMAGE_WIDTH

    if width <= max_width and height <= max_height:
        return {'width': width, 'height': height}
    else:

        if width > height:
            height = reduce_dimension(width, max_width, height) if height > max_height else height
            width = max_width

        elif height > width:
            width = reduce_dimension(height, max_height, width) if width > max_width else width
            height = max_height
        else:
            if max_width > max_height:
                width = max_width
                height = width
            else:
                height = max_height
                width = height

        return {'width': width, 'height': height}

def generate_url_with_dimensions(url, dimensions):
    return "src=\"%s\"" % generate_url(url, height=dimensions['height'], width=dimensions['width'])

def replace_pc(m):

    url = m.group("url")

    height = m.group("height")
    width = m.group("width")

    return generate_url_with_dimensions(url, reduce_proportionally(int(width), int(height), False))

def replace_mobile(m):

    url = m.group("url")

    height = m.group("height")
    width = m.group("width")



    return generate_url_with_dimensions(url, reduce_proportionally(int(width), int(height), True))



@register.simple_tag(takes_context=True)
def thumbor_replace(context, text):

    user_agent = get_user_agent(context['request'])

    regex = regex_pattern_with_style if regex_pattern_with_style.match(text) else regex_pattern_with_attribute


    return mark_safe(regex.sub(replace_mobile if user_agent.is_mobile else replace_pc, text))