__author__ = 'phillip'

import re
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()

class NotValidURI(Exception):
    pass

class SiteUrlNotFound(Exception):
    pass

class URI():
    uri_regex = re.compile(r'((?P<scheme>\w+)://)?(?P<domain>[\w.-]+)?(:(?P<port>\d+))?(?P<path>[/[\w-]*(.(?P<content_type>[\w-]+))*)$')

    def __init__(self, uri=None):

        self.uri =  self.uri_regex.match(uri)

        if not self.uri:
            raise NotValidURI("String is not a valid uri")

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
@stringfilter
def absolute(value):
    if not hasattr(settings, "SITE_URL"):
        raise SiteUrlNotFound("SITE_URL setting in settings.py is not definied!")
    return URI(settings.SITE_URL+value).absolute_uri


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