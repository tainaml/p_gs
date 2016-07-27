from django.conf import settings
from django.core.cache import caches, cache
from abc import ABCMeta, abstractmethod


class CacheItemMixin(object):

    __metaclass__ = ABCMeta

    expiration = None

    def __init__(self, cache_name='default'):
        self.cache = cache

    @abstractmethod
    def get_cache_key(self):
        return ''

    @abstractmethod
    def generate_new_cache(self):
        return ''

    def get_from_cache(self):
        return self.cache.get(self.get_cache_key())

    def set_to_cache(self, content=None, expires=None):
        if not expires:
            expires = self.expiration
        if not content:
            content = self.generate_new_cache()
        self.cache.set(self.get_cache_key(), content, expires)
        return content

    def get_from_cache_or_create(self, expires=None):
        from_cache = self.cache.get(self.get_cache_key(), False)
        if not from_cache:
            from_cache = self.generate_new_cache()
            self.set_to_cache(from_cache)
        return from_cache

    def invalidate_cache(self):
        self.cache.delete(self.get_cache_key())

    def recreate_cache(self):
        self.set_to_cache()


class CacheControl(object):

    CACHE_GROUPS = 'CACHE_GROUPS'

    def __init__(self):
        self._groups = {}
        self.cache = cache

    def add_to_group(self, group, item):
        cache_groups = self.cache.get(self.CACHE_GROUPS, {})
        groups = cache_groups.get(group, [])
        groups.append(item)
        groups = list(set(groups))
        cache_groups.update({
            group: groups
        })
        self.cache.set(self.CACHE_GROUPS, cache_groups, None)

    def get_all(self):
        return self.cache.get(self.CACHE_GROUPS, {})

    def has_group(self, group):
        cache_groups = self.cache.get('CACHE_GROUPS', {})
        return cache_groups.has_key(group)

    def get_group(self, group):
        cache_groups = self.cache.get('CACHE_GROUPS', {})
        return cache_groups.get(group, [])

    def __broadcast_clear_item(self, item):
        for group in self._groups.itervalues():
            if item in group:
                group.remove(item)

    def clear_group(self, group, broadcast_item_clear=True):
        groups = self.get_group(group)
        for item in groups:
            item.recreate_cache()
            if broadcast_item_clear:
                self.__broadcast_clear_item(item)

        self._groups.update({
            group: []
        })

cachecontrol = CacheControl()