from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import itertools


class ContentTypeCached():

    class objects():

        _all = None

        @classmethod
        def _get_opts(cls, model):
            model = model._meta.concrete_model
            return model._meta

        @classmethod
        def all(cls):
            if cls._all is None:
                articles_question = ContentType.objects.filter(Q(model__in=['article', 'question'])).order_by("model")
                comment = ContentType.objects.filter(Q(model='comment'))
                rest = ContentType.objects.all().exclude(Q(model__in=["article", "question", "comment"]))
                content_types = list(itertools.chain(articles_question, comment, rest))

                cls._all = content_types
                rest = cache.set("content_type", cls._all)
            return cls._all

        @classmethod
        def get_for_model(cls, model=None):
            opts = cls._get_opts(model=model)
            return cls.get(model=opts.model_name)

        @classmethod
        def filter(cls, model__in=None):
            if not model__in:
                model__in = []
            content_types = []
            for content_type in cls.all():
                if not model__in:
                    break
                if content_type.model in model__in:
                    content_types.append(content_type)
                    model__in.remove(content_type.model)


            return content_types

        @classmethod
        def get(cls, model=None):
            for content_type in cls.all():
                if content_type.model == model:
                    return content_type

            return None









