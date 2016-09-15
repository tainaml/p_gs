from django.core.cache import cache
from django.db import models
from django.contrib.contenttypes.models import ContentType

class ContentTypeCachedSingleton():

    class objects():

        _all = None

        @classmethod
        def all(cls):
            if cls._all is None:
                cls._all = ContentType.objects.all()
                cache.set("content_type", cls._all)
            return cls._all









