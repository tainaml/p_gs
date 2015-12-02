from abc import ABCMeta, abstractmethod, abstractproperty
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import Node
from django.template.loader import render_to_string
from django.utils import timezone
from apps.article.models import Article
from apps.feed.models import FeedObject
from apps.taxonomy.models import Taxonomy
from rede_gsti import settings

register = template.Library()

class AbstractHomeBlock(object):

    __metaclass__ = ABCMeta

    template_file = ''

    def __init__(self, category_slug):
        self.category_slug = category_slug

    @abstractproperty
    def template_file(self):
        return self.template_file

    def filter_articles(self, quantity = 3, offset = 0):
        pass


class BlockFullWidth(AbstractHomeBlock):

    template_file = 'home/blocks/block-full-width.html'

    def teste(self):
        return 1


class BlockHalfTwo(AbstractHomeBlock):

    template_file = 'home/blocks/block-half-two.html'


home_blocks_templates = {
    'block-full-width': BlockFullWidth,
    'block-half-two': BlockHalfTwo
}


@register.simple_tag()
def home_block(block_type, category_slug, quantity_categories=4, offset=0, class_name="without-class"):
    context = {}

    context.update(class_name=class_name)

    block = home_blocks_templates.get(block_type, None)
    if block is None:
        return 'block is none'

    category = []
    try:
        category = Taxonomy.objects.get(slug=category_slug)
    except Taxonomy.DoesNotExist, e:
        return 'Nao Existe'

    article_type = ContentType.objects.get(model="article")

    articles = Article.objects.filter(
        pk__in=FeedObject.objects.filter(
            #taxonomies=category,
            content_type=article_type,
        ),
        status=Article.STATUS_PUBLISH,
        publishin__lte=timezone.now()
    ).order_by('-id')[offset:quantity_categories]

    context.update({
        'category': category,
        'articles': articles.all()
    })

    template = render_to_string(block.template_file, context)
    return template


@register.simple_tag()
def home_block_full_width(*args, **kwargs):
    return home_block('block-full-width', *args, **kwargs)

@register.simple_tag()
def home_block_half_two(*args, **kwargs):
    return home_block('block-half-two', *args, **kwargs)