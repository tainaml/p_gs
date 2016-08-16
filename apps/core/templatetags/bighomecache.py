# -*- coding: utf-8 -*-
from django import template
from django.core.cache import cache
from django.template.library import SimpleNode
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from apps.core.cachecontrol import CacheItemMixin, cachecontrol

register = template.Library()


class HomeCacheNode(CacheItemMixin, template.Node):

    excludes = []

    def __init__(self, nodelist, token, page='home'):
        self.nodelist = nodelist
        self.token = token
        self.page = page
        super(HomeCacheNode, self).__init__()

    def generate_new_cache(self, context=None):
        return self.do_render(context)

    def set_to_cache(self, content=None, expires=None, context=None):
        if not expires:
            expires = self.expiration
        if not content:
            content = self.generate_new_cache(context)
        self.cache.set(self.get_cache_key(), content, expires)
        return content

    def get_from_cache_or_create(self, expires=None, context=None):
        from_cache = self.cache.get(self.get_cache_key(), False)
        if not from_cache:
            from_cache = self.generate_new_cache(context)
            self.set_to_cache(from_cache, context=context)
        return from_cache

    def get_cache_key(self):
        return 'gsti|excludes|%s' % self.page

    def do_render(self, context):

        content = ''

        __excludes = []

        context.update({'excludes': __excludes, 'clear_cache': True})

        for node in self.nodelist:
            content += force_unicode(node.render(context))

        return mark_safe(content)

    def render(self, context):

        category = context.get('category', None)
        if category:
            self.page = category.slug

        return self.get_from_cache_or_create(context=context)

@register.tag()
def bighomecache(parser, token):

    nodelist = parser.parse(('endbighomecache',))
    parser.delete_first_token()

    return HomeCacheNode(nodelist, token)
