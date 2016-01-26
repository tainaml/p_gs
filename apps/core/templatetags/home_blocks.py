from abc import ABCMeta
from itertools import chain

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models import Q, Prefetch
from django.template.loader import render_to_string
from django.utils import timezone

from apps.article.models import Article
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from apps.taxonomy.service import business as TaxonomyBusiness

register = template.Library()
article_type = ContentType.objects.get(model="article")

cache = caches['default']

home_block_counter = 0

home_block_excludes = []


class AbstractHomeBlock(object):

    __metaclass__ = ABCMeta

    template_file = ''
    context = {}

    block_name = ''

    __context = {}

    def __init__(self, category, quantity=3, cache_time=0, offset=0, show_comunities=4, class_name="without-class", template=None):

        if not self.block_name:
            self.block_name = self.__class__.__name__

        self.category_slug = category
        self.class_name = class_name
        self.quantity = quantity
        self.offset = offset
        self.show_comunities = show_comunities
        self.class_name = class_name
        self.cache_time = cache_time

        if template is not None:
            self.template_file = template

        if not isinstance(category, Taxonomy):
            category = self.get_category(category)

        self.category = category


    def get_category(self, category_slug):
        try:
            category = Taxonomy.objects.get(slug=category_slug)
            return category
        except Taxonomy.DoesNotExist, notExistTaxonomy:
            return None

    @property
    def custom_filters(self):
        return Q(
            feed__content_type=article_type,
            publishin__lte=timezone.now(),
            feed__taxonomies__in=[self.category],
            status__in=[Article.STATUS_PUBLISH, Article.STATUS_DRAFT]
        )

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

        communities_filters = dict(
            taxonomy=self.category
        )

        communities = Community.objects.filter(**communities_filters)

        excludes_key = 'home_block_excludes_%s' % self.category.slug.lower()
        excludes = cache.get(excludes_key, [])
        excludes = sorted(set(excludes))

        articles = Article.objects.filter(
            self.custom_filters
        ).exclude(
            pk__in=sorted(set(home_block_excludes)) # POG: pensar numa forma melhor de evitar duplicatas na home
        ).order_by(
            self.custom_order
        ).prefetch_related(
            Prefetch('feed__communities', queryset=communities),
        )[self.offset:self.quantity + self.offset]

        for article in articles:
            excludes.append(article.pk)

        cache.set(excludes_key, excludes)

        context = {
            'class_name': self.class_name,
            'articles': articles,
            'category': self.category
        }

        self.context.update(context)

    def get_communities(self):

        if not self.show_comunities:
            return False

        taxonomies = self.get_taxonomies()

        try:
            communities = Community.objects.filter(
                taxonomy__in=taxonomies
            ).order_by('taxonomy')[0:self.show_comunities]
        except Community.DoesNotExist, e:
            communities = False


        return communities

    def get_context(self):
        return self.context

    def render(self):

        # cache_key = make_template_fragment_key(self.block_name, (
        #     self.category.slug.lower(),
        # ))
        # workaround
        if not self.category:
            print self.category
            return ''

        cache_key = self.block_name + "-" + self.category.slug.lower()
        template = cache.get(cache_key)

        template = False # Uncomment to run without cache

        if not template:
            self.filter_articles()
            template = render_to_string(self.template_file, context=self.get_context())
            cache.set(cache_key, template, self.cache_time)

        return template

class ArticleCommunityPartial(AbstractHomeBlock):

    template_file = 'home/blocks/partials/article_community.html'

    def __init__(self, article, category, template=None):

        self.article = article

        super(ArticleCommunityPartial, self).__init__(category, show_comunities=True, template=template)

    def render(self):

        taxs = self.get_taxonomies()

        communities = Community.objects.filter(
            taxonomy__in=taxs
        ).order_by('?')

        self.get_context().update({
            'article': self.article,
            'community': communities.first()
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

class BlockHighlightLarge(AbstractHomeBlock):
    template_file = 'home/blocks/block-article-home-large.html'
    block_name = 'home_block_article_home'

@register.simple_tag()
def home_block(block_class, category_slug, quantity=None, cache_time=None, show_comunities=None, offset=0, class_name="without-class", template=None):
    block = block_class(category_slug, quantity, cache_time, offset, show_comunities, class_name, template)
    return block.render()

@register.simple_tag()
def home_block_full_width(*args, **kwargs):
    return home_block(BlockFullWidth, *args, **kwargs)

@register.simple_tag()
def home_block_half_two(*args, **kwargs):
    return home_block(BlockHalfTwo, *args, **kwargs)

@register.simple_tag()
def home_block_half_three(*args, **kwargs):
    return home_block(BlockHalfThree, *args, **kwargs)

@register.simple_tag()
def home_block_third(*args, **kwargs):
    return home_block(BlockThird, *args, **kwargs)

@register.simple_tag()
def home_block_highlight_simple(*args, **kwargs):
    template = kwargs.get('template', 'home/blocks/block-highlight-simple.html')
    kwargs.update(template=template)
    kwargs.update(show_comunities=False)
    return home_block(BlockHighlight, *args, **kwargs)

@register.simple_tag()
def home_block_highlight_with_image(*args, **kwargs):
    template = kwargs.get('template', 'home/blocks/block-highlight-with-image.html')
    kwargs.update(template=template)
    kwargs.update(show_comunities=False)
    return home_block(BlockHighlight, *args, **kwargs)

@register.simple_tag()
def home_block_article_home(*args, **kwargs):
    return home_block(BlockHighlightLarge, *args, **kwargs)

@register.simple_tag(name="home_article_community")
def home_article_community(article, category):
    bloco = ArticleCommunityPartial(category, article)
    return bloco.render()