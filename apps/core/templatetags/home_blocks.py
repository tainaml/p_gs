from abc import ABCMeta
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models import Q, Prefetch, QuerySet
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import FeedObject
from ..utils import generate_home_cache_key
from apps.article.models import Article
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from apps.taxonomy.service import business as TaxonomyBusiness
from django.conf import settings
from ..cachecontrol import cachecontrol, CacheItemMixin


register = template.Library()
article_type = ContentTypeCached.objects.get(model="article")

cache = caches['default']

home_block_counter = 0

# home_block_excludes = []


class ExcludesHomeItems(CacheItemMixin):

    __cache_key = None
    __excludes = []

    def __init__(self, cache_key):

        self.__cache_key = cache_key
        super(ExcludesHomeItems, self).__init__()

    def add_excludes(self, excludes):
        self.__excludes = list(set(excludes))

    def get_cache_key(self):
        return self.__cache_key

    def generate_new_cache(self):
        return []

    def get_from_cache(self):
        val = super(ExcludesHomeItems, self).get_from_cache()
        if not val:
            val = self.generate_new_cache()
        return val


class AbstractHomeBlock(CacheItemMixin):
    __metaclass__ = ABCMeta

    template_file = ''
    context = {}

    block_name = ''

    __context = {}

    def __init__(self, context, category, quantity=3, cache_time=0, offset=0, show_comunities=4, class_name="without-class",
                 template=None):

        if not self.block_name:
            self.block_name = self.__class__.__name__

        self.category_slug = category
        self.class_name = class_name
        self.quantity = quantity
        self.offset = offset
        self.show_comunities = show_comunities
        self.class_name = class_name
        self.cache_time = cache_time

        # self.category = self.get_category(self.category_slug)
        if not isinstance(category, Taxonomy):
            category = self.get_category(category)

        self.category = category

        # self.cache_home_page = 'default'
        self.cache_home_page = 'home'

        if 'request' in context and context['request'].path != u'/':
            self.cache_home_page = self.category_slug

        self.cache_home_page = 'homehome_excludes__%s' % self.cache_home_page

        self.cache = caches['default']

        global_excludes = cache.get('global_home_excludes', [])
        global_excludes.append(self.cache_home_page)
        cache.set('global_home_excludes', sorted(set(global_excludes)), None)

        super(AbstractHomeBlock, self).__init__()

        # self.cache_home_page = self.cache_home_page

        cachecontrol.add_to_group('global_home::%s' % self.category_slug, self)

        # cachecontrol.add_to_group('global_excludes', self)


        if template is not None:
            self.template_file = template

    def get_cache_key(self):
        return '%s-%s-%s' % (
            self.block_name,
            self.cache_home_page,
            self.category_slug
        )

    def generate_new_cache(self):
        return self.__render()

    def get_category(self, category_slug):
        try:
            category = Taxonomy.objects.get(slug=category_slug, term__description='Categoria')
            return category
        except Taxonomy.DoesNotExist, notExistTaxonomy:
            return None

    @property
    def custom_filters(self):

        communities = Community.objects.filter(
            Q(taxonomy__parent__id=self.category.id) | \
            Q(taxonomy__id=self.category.id)
        )

        q = Q(
            feed__official=True,
            feed__communities__in=communities,
            status__in=[Article.STATUS_PUBLISH],
            feed__content_type=article_type,
            publishin__lte=timezone.now(),
        )

        return q

    def get_taxonomies(self):

        taxonomies = []
        if self.show_comunities is not None:
            taxonomies = TaxonomyBusiness.get_related_list_top_down((self.category,))

        return taxonomies

    @property
    def custom_order(self):
        return '-publishin'

    @property
    def context(self):
        return self.__context

    def filter_articles(self):

        __communities = self.get_communities()

        self.context.update({
            'communities': __communities
        })

        if self.category is None:
            return False

        communities_filters = Q(taxonomy__parent__id=self.category.id) | \
                              Q(taxonomy__id=self.category.id)

        communities = Community.objects.filter(communities_filters)

        excludes = self.cache.get(self.cache_home_page, [])
        excludes = sorted(set(excludes))

        excludes_cache = ExcludesHomeItems(self.cache_home_page)
        excludes = excludes_cache.get_from_cache_or_create()

        articles = Article.objects.filter(
            self.custom_filters
        ).exclude(
            id__in=excludes
        ).order_by(
            self.custom_order
        ).prefetch_related(
            Prefetch('feed__communities', queryset=communities),
        ).distinct()[self.offset:self.quantity + self.offset]

        #excludes = []

        for article in articles:
            excludes.append(article.pk)
            if not article.image:
                feed = FeedObject.objects.get(article=article)
                communities = Community.objects.filter(
                    feeds=feed
                ).prefetch_related("taxonomy")
                article.image = communities[0].image

        # excludes_cache.add_excludes(excludes)
        # cachecontrol.add_to_group('os_excludes', excludes_cache)

        self.cache.set(self.cache_home_page, excludes, None)

        context = {
            'class_name': self.class_name,
            'articles': articles,
            'category': self.category
        }

        self.context.update(context)

    def filter_communities(self):

        communities = Community.objects.filter(
            Q(taxonomy__parent__id=self.category.id) | \
            Q(taxonomy__id=self.category.id)
        )

        return communities

    def get_communities(self):

        if not self.show_comunities:
            return False

        try:

            communities = self.filter_communities().order_by('?')[0:self.show_comunities]

        except Community.DoesNotExist, e:
            communities = False

        return communities

    def get_context(self):
        return self.context


    def __render(self):

        if not self.category_slug:
            return ''

        self.filter_articles()
        template = render_to_string(self.template_file, context=self.get_context())

        return mark_safe(template)

    def render(self):

        if not self.category_slug:
            return ''

        #cachecontrol.add_to_group(self.cache_home_page, self)
        return mark_safe(self.get_from_cache_or_create())


class ArticleCommunityPartial(AbstractHomeBlock):
    template_file = 'home/blocks/partials/article_community.html'

    def __init__(self, context, article, category, template=None):
        self.article = article
        self.__category = category

        super(ArticleCommunityPartial, self).__init__(context, category, show_comunities=True, template=template)

    def render(self):

        communities = self.filter_communities().order_by('?')
        the_community = communities.first() if communities.count() > 0 else None

        try:
            the_communities = self.article.feed.all()
            the_communities = the_communities.filter(taxonomy=self.__category)
            the_community = the_communities.first()
        except Exception, e:
            pass

        self.get_context().update({
            'article': self.article,
            'community': the_community
        })

        return render_to_string(self.template_file, context=self.get_context())


class BlockFullWidth(AbstractHomeBlock):
    template_file = 'home/blocks/block-full-width.html'
    block_name = 'home_block_full_width'


class BlockHalfTwo(AbstractHomeBlock):
    template_file = 'home/blocks/block-half-two.html'
    block_name = 'home_block_half_two'


class BlockHalfThree(AbstractHomeBlock):
    template_file = 'home/blocks/block-half-three.html'
    block_name = 'home_block_half_three'


class BlockThird(AbstractHomeBlock):
    template_file = 'home/blocks/block-third.html'
    block_name = 'home_block_third'


class BlockHighlight(AbstractHomeBlock):
    template_file = 'home/blocks/highlight-simple.html'
    block_name = 'home_block_highlight'


class BlockHighlightSimple(AbstractHomeBlock):
    template_file = 'home/blocks/block-highlight-simple.html'
    block_name = 'home_block_highlight_simples'


class BlockHighlightWithImage(AbstractHomeBlock):
    template_file = 'home/blocks/block-highlight-with-image.html'
    block_name = 'home_block_highlight_image'


class BlockHighlightLarge(AbstractHomeBlock):
    template_file = 'home/blocks/block-article-home-large.html'
    block_name = 'home_block_article_home'


@register.simple_tag(takes_context=True)
def home_block(block_class, context, category_slug, quantity=None, cache_time=None, show_comunities=None, offset=0,
               class_name="without-class", template=None):
    #block = block_class(context, category_slug, quantity, cache_time, offset, show_comunities, class_name, template)
    #return block.render()
    return ''


@register.simple_tag(takes_context=True)
def home_block_full_width(context, *args, **kwargs):
    return home_block(BlockFullWidth, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_half_two(context, *args, **kwargs):
    return home_block(BlockHalfTwo, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_half_three(context, *args, **kwargs):
    return home_block(BlockHalfThree, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_third(context, *args, **kwargs):
    return home_block(BlockThird, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_highlight_simple(context, *args, **kwargs):
    kwargs.update(show_comunities=False)
    return home_block(BlockHighlightSimple, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_highlight_with_image(context, *args, **kwargs):
    kwargs.update(show_comunities=False)
    return home_block(BlockHighlightWithImage, context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def home_block_article_home(context, *args, **kwargs):
    return home_block(BlockHighlightLarge, context, *args, **kwargs)


@register.simple_tag(takes_context=True, name="home_article_community")
def home_article_community(context, article, category):
    bloco = ArticleCommunityPartial(context, category, article)
    return bloco.render()