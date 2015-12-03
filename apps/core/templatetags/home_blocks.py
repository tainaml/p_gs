from abc import ABCMeta
from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.template.loader import render_to_string
from django.utils import timezone
from apps.article.models import Article
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from apps.taxonomy.service import business as TaxonomyBusiness

register = template.Library()
article_type = ContentType.objects.get(model="article")

class AbstractHomeBlock(object):

    __metaclass__ = ABCMeta

    template_file = ''
    context = {}

    __context = {}

    def __init__(self, category, quantity=3, offset=0, show_comunities=4, class_name="without-class"):
        self.category_slug = category
        self.class_name = class_name
        self.quantity = quantity
        self.offset = offset
        self.show_comunities = show_comunities
        self.class_name = class_name

        self.category = self.get_category()

    def get_category(self):
        try:
            category = Taxonomy.objects.get(slug=self.category_slug)
            return category
        except Taxonomy.DoesNotExist, notExistTaxonomy:
            return None

    @property
    def custom_filters(self):
        return Q(
            feed__taxonomies__in=[self.category],
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

        if self.show_comunities:
            taxonomies = self.get_taxonomies()

            communities = []

            try:
                communities = Community.objects.filter(

                ).order_by('taxonomy')
            except Community.DoesNotExist, e:
                pass

            self.context.update({
                'communities': communities
            })

        self.context.update({
            'class_name': self.class_name,
            'articles': articles,
            'category': self.category
        })

    def get_context(self):
        return self.context

    def render(self):
        self.filter_articles()
        template = render_to_string(self.template_file, context=self.get_context())
        return template


class BlockFullWidth(AbstractHomeBlock):

    template_file = 'home/blocks/block-full-width.html'


class BlockHalfTwo(AbstractHomeBlock):

    template_file = 'home/blocks/block-half-two.html'


@register.simple_tag()
def home_block(block_class, category_slug, quantity=None, show_categories=None, offset=0, class_name="without-class"):
    block = block_class(category_slug, quantity, offset, 4, class_name)
    return block.render()

@register.simple_tag()
def home_block_full_width(*args, **kwargs):
    return home_block(BlockFullWidth, *args, **kwargs)

@register.simple_tag()
def home_block_half_two(*args, **kwargs):
    return home_block(BlockHalfTwo, *args, **kwargs)