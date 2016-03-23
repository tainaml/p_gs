from __future__ import unicode_literals
from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.utils import make_template_fragment_key
from django.template import (
    Library, Node, TemplateSyntaxError, VariableDoesNotExist,
)

register = Library()

cache = caches['default']


class IdeiaHomeCacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on, cache_name):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.cache_name = cache_name

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag got an unknown variable: %r' % self.expire_time_var.var)

        if expire_time is not None:
            try:
                expire_time = int(expire_time)
            except (ValueError, TypeError):
                raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % expire_time)

        fragment_cache = cache

        vary_on = [var.resolve(context) for var in self.vary_on]
        cache_key = make_template_fragment_key(self.fragment_name, vary_on)

        global_cache = fragment_cache.get('home_page_caches', [])
        global_cache.append(cache_key)
        fragment_cache.set('home_page_caches', global_cache, None)

        value = fragment_cache.get(cache_key)
        if value is None:
            value = self.nodelist.render(context)
            fragment_cache.set(cache_key, value, expire_time)
        return value


@register.tag('ideiahomecache')
def ideia_do_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.

    Usage::

        {% load ideiahomecache %}
        {% ideiahomecache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endideiahomecache %}

    This tag also supports varying by a list of arguments::

        {% load ideiahomecache %}
        {% ideiahomecache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endideiahomecache %}

    Optionally the cache to use may be specified thus::

        {% ideiahomecache ....  using="cachename" %}

    Each unique set of arguments will result in a unique cache entry.
    """
    nodelist = parser.parse(('endideiahomecache',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments." % tokens[0])
    if len(tokens) > 3 and tokens[-1].startswith('using='):
        cache_name = parser.compile_filter(tokens[-1][len('using='):])
        tokens = tokens[:-1]
    else:
        cache_name = None
    return IdeiaHomeCacheNode(nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(t) for t in tokens[3:]],
        cache_name,
    )
