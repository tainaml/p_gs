from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models import Q, Prefetch
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from apps.article.models import Article
from apps.community.models import Community
from apps.feed.models import FeedObject
from apps.taxonomy.models import Taxonomy
from ..cachecontrol import cachecontrol, CacheItemMixin


register = template.Library()
article_type = ContentType.objects.get(model="article")

cache_excludes_prefix = 'HOME_EXCLUDES|||%s'

class ArticleCacheExcludes(object):

    prefix = 'HOME_EXCLUDES|||%s'

    cache = caches['default']

    def __init__(self):
        pass

    @classmethod
    def get(cls, home):
        print cls.prefix % home
        excludes = cls.cache.get(cls.prefix % home, [])
        return excludes


    @classmethod
    def append(cls, home, excludes):
        _excludes = cls.cache.get(cls.prefix % home, [])
        for ex in excludes:
            _excludes.append(ex)

        _excludes = list(set(_excludes))

        cls.cache.set(cls.prefix % home, _excludes, None)


    @classmethod
    def clear(cls, home):
        print cls.prefix % home
        cls.cache.delete(cls.prefix % home)


class ArticleBlock(CacheItemMixin):

    def __init__(self, context, type, category_slug, quantity=0, cache_time=None,
                  show_communities=None, offset=0, class_name="without-class", differ="a", template=None):

        self.type = type
        self.category_slug = category_slug
        self.category = self.get_category(category_slug)
        self.quantity = quantity
        self.cache_time = cache_time
        self.show_communities = show_communities
        self.offset = offset
        self.class_name = class_name
        self.template = template
        self.differ = differ

        self.__context = {}

        self.cache_excludes = 'home'

        if 'request' in context and context['request'].path != u'/':
            self.cache_excludes = self.category_slug

        print self.cache_excludes

        super(ArticleBlock, self).__init__()

    def get_cache_key(self):
        return '%s::%s::%s::%s' % (
            str(self.type),
            str(self.cache_excludes),
            str(self.category_slug),
            str(self.differ),
        )

    def generate_new_cache(self):
        return self.__render()

    def get_category(self, category_slug):
        try:
            category = Taxonomy.objects.get(slug=category_slug, term__description='Categoria')
            return category
        except Taxonomy.DoesNotExist, notExistTaxonomy:
            return None

    def get_communities(self):
        communities_filters = Q(taxonomy__parent__slug=self.category_slug) | Q(taxonomy__slug=self.category_slug)
        communities = Community.objects.filter(communities_filters)
        return communities

    def get_show_communities(self):
        communities = self.get_communities().order_by('?')[0:self.show_communities]
        print communities
        return communities

    def filter_articles(self):

        communities = self.get_communities()

        excludes = ArticleCacheExcludes.get(self.cache_excludes)

        articles = Article.objects.filter(
            self.custom_filters
        ).exclude(
            id__in=excludes
        ).order_by(
            self.custom_order
        ).prefetch_related(
            Prefetch('feed__communities', queryset=communities),
        ).distinct()[self.offset:self.quantity + self.offset]

        # [excludes.append(article.id) for article in articles]

        for article in articles:
            excludes.append(article.id)
            if not article.image:
                feed = FeedObject.objects.get(article=article)
                communities = Community.objects.filter(
                    feeds=feed
                ).prefetch_related("taxonomy")
                article.image = communities[0].image

        ArticleCacheExcludes.append(self.cache_excludes, excludes)

        context = {
            'class_name': self.class_name,
            'articles': articles,
            'category': self.category,
            'communities': self.get_show_communities()
        }

        self.get_context().update(context)

    @property
    def custom_filters(self):

        communities = self.get_communities()

        q = Q(
            feed__official=True,
            feed__communities__in=communities,
            status__in=[Article.STATUS_PUBLISH],
            feed__content_type=article_type,
            publishin__lte=timezone.now(),
        )
        return q

    @property
    def custom_order(self):
        return '-publishin'

    def get_context(self):
        return self.__context

    def __render(self):
        self.filter_articles()
        template = render_to_string(self.template, context=self.get_context())
        return template

    def render(self):
        cachecontrol.add_to_group('global_home::%s' % self.cache_excludes, self)
        return mark_safe(self.get_from_cache_or_create())


MAPPER_CLASS = {
    'default': ArticleBlock
}


@register.simple_tag(takes_context=True)
def article_block(context, type, category_slug, **kwargs):

    if kwargs.get('template', None) is None:
        kwargs.update({'template': 'home/blocks/article/%s.html' % type})

    block_class = MAPPER_CLASS.get('default')
    if type in MAPPER_CLASS:
        block_class = MAPPER_CLASS.get('type')

    block_item = block_class(context, type, category_slug, **kwargs)

    return block_item.render()