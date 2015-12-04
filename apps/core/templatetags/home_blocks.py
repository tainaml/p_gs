from abc import ABCMeta
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import get_cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models import F, Q
from django.template.loader import render_to_string
from django.utils import timezone
from apps.article.models import Article
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from apps.taxonomy.service import business as TaxonomyBusiness

register = template.Library()
article_type = ContentType.objects.get(model="article")

cache = get_cache('default')

class AbstractHomeBlock(object):

    __metaclass__ = ABCMeta

    template_file = ''
    context = {}

    block_name = ''

    __context = {}

    def __init__(self, category, quantity=3, cache_time=0, offset=0, show_comunities=4, class_name="without-class"):

        if not self.block_name:
            self.block_name = self.__class__.__name__

        self.category_slug = category
        self.class_name = class_name
        self.quantity = quantity
        self.offset = offset
        self.show_comunities = show_comunities
        self.class_name = class_name
        self.cache_time = cache_time
        self.category = self.get_category()

    def get_category(self):
        try:
            category = Taxonomy.objects.get(slug=self.category_slug)
            return category
        except Taxonomy.DoesNotExist, notExistTaxonomy:
            return None

    @property
    def custom_filters(self):
        #feed__taxonomies__in=[self.category],
        return Q(
            feed__content_type=article_type,
            publishin__lte=timezone.now(),
            status=Article.STATUS_PUBLISH
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

        if self.category is None:
            return False

        articles = Article.objects.filter(self.custom_filters).order_by(self.custom_order)[self.offset:self.quantity]

        context = {
            'class_name': self.class_name,
            'articles': articles,
            'category': self.category
        }

        self.context.update(context)


    def filter_communities(self):

        if not self.show_comunities:
            return

        taxonomies = self.get_taxonomies()

        try:
            communities = Community.objects.filter(
                taxonomy__in=taxonomies
            ).order_by('taxonomy')[0:self.show_comunities]
        except Community.DoesNotExist, e:
            communities = False

        self.context.update({
            'communities': communities
        })

    def get_context(self):
        return self.context

    def render(self):

        cache_key = make_template_fragment_key(self.block_name, (
            self.class_name,
            self.category,
        ))

        template = cache.get(cache_key)

        if not template:
            self.filter_articles()
            self.filter_communities()
            template = render_to_string(self.template_file, context=self.get_context())
            cache.set(cache_key, template, self.cache_time)

        return template


class BlockFullWidth(AbstractHomeBlock):

    template_file = 'home/blocks/block-full-width.html'
    block_name = 'home_block_full_width'


class BlockHalfTwo(AbstractHomeBlock):

    template_file = 'home/blocks/block-half-two.html'
    block_name = 'home_block_half_two'


class BlockHalfThree(AbstractHomeBlock):

    template_file = 'home/blocks/block-half-three.html'
    block_name = 'home_block_half_three'

    def get_context(self):

        articles = self.context.get('articles', [])

        self.context.update({
            'articles_master': articles[0:3],
            'articles_others': articles[3:] if len(articles) > 3 else []
        })

        return self.context


@register.simple_tag()
def home_block(block_class, category_slug, quantity=None, cache_time=0, show_comunities=None, offset=0, class_name="without-class"):
    block = block_class(category_slug, quantity, cache_time, offset, show_comunities, class_name)
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