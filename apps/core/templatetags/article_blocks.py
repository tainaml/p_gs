import copy
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models import Q, Prefetch, QuerySet
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from apps.article.models import Article
from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import FeedObject
from apps.taxonomy.models import Taxonomy
from ..cachecontrol import cachecontrol, CacheItemMixin


register = template.Library()

article_type = None

try:
    article_type = ContentTypeCached.objects.get(model="article")
except:
    pass

cache_excludes_prefix = 'HOME_EXCLUDES|||%s'

class ArticleCacheExcludes(object):

    prefix = 'HOME_EXCLUDES|||%s'

    cache = caches['default']

    def __init__(self):
        pass

    @classmethod
    def get(cls, home):
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
        cls.cache.delete(cls.prefix % home)


def get_article_community_by_category(article, category):

    try:
        the_community = article.feed.all().first().communities.all().filter(Q(taxonomy_id=category.id) | Q(taxonomy__parent_id=category.id)).first()
    except Exception, e:
        the_community = None

    return the_community


class ArticleBlock(CacheItemMixin):

    def __init__(self, context, type, category_slug, quantity=0,
                 cache_time=None, show_communities=None, offset=0,
                 class_name="without-class", excludes=None, differ="a", template=None):

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

        self.excludes = context.get('excludes', [])
        self.clear_cache = context.get('clear_cache', False)

        self.cache_excludes = 'home'

        if 'request' in context and context['request'].path != u'/':
            self.cache_excludes = self.category_slug

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
        return communities

    def filter_articles(self):

        communities = self.get_communities()

        articles = Article.objects.filter(
            self.custom_filters
        ).exclude(
            id__in=self.excludes
        ).order_by(
            self.custom_order
        ).prefetch_related(
            Prefetch('feed__communities', queryset=communities),
        ).distinct()[self.offset:self.quantity + self.offset]

        for article in articles:
            # context_excludes.append(article.id)
            self.excludes.append(article.id)

            if not article.image:
                _community = get_article_community_by_category(article, self.category)
                article.image = _community.image if _community else None

        # ArticleCacheExcludes.append(self.cache_excludes, excludes)
        # self.base_context.update({'excludes': context_excludes})

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

        return mark_safe(self.__render())
        #if self.clear_cache:
        # self.invalidate_cache()
        # return mark_safe(self.get_from_cache_or_create())


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


@register.simple_tag(takes_context=True)
def article_block_show(context, type, items, category_slug, **kwargs):

    template_file = kwargs.get('template', 'home/blocks/article/{}.html'.format(type))

    data = {}

    articles = context.get(items)
    articles_count = len(articles)

    quantity = kwargs.get('quantity')

    if quantity > articles_count:
        quantity = articles_count

    filtered_articles = articles[0:quantity]

    articles = [article for article in articles if article not in filtered_articles]

    data.update({
        'articles': filtered_articles
    })

    context.update({
        'articles': articles
    })

    return mark_safe(
        render_to_string(
            template_name=template_file,
            context=data,
            request=context.get('request')
        )
    )


@register.simple_tag(takes_context=True)
def article_community_block(context, category, article, **kwargs):

    the_community = get_article_community_by_category(article, category)

    __context = {
        'article': article,
        'community': the_community
    }

    template_file = kwargs.get('template', 'home/blocks/partials/article_community.html')

    return render_to_string(template_file, __context)


@register.inclusion_tag('home/blocks/partials/communities.html', takes_context=True)
def communities(context, communities):

    space_between = communities.count() if isinstance(communities, (QuerySet)) else len(communities)
    MAXIMUM = getattr(settings, 'HOME_CHARACTERS_LIMIT', 0) - space_between
    communities_to_show = []
    character_counting = 0

    for community in communities:
        char_quantity = len(community.title)
        character_counting += char_quantity
        if character_counting > MAXIMUM:
            break
        communities_to_show.append(community)

    return {
        'communities': communities_to_show
    }