from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models import Q, Prefetch
from django.utils import timezone
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.taxonomy.models import Taxonomy

cache = caches['default']
article_type = ContentTypeCached.objects.get(model="article")

class HomePageAbstract(object):

    cache_prefix = 'home_cache_%s'
    cache_key = 'default'

    def __init__(self, *args, **kwargs):
        self.register_cache()

    def register_cache(self):
        homes_all_cache = cache.get('homes_all_cache', [])
        homes_all_cache.append(self.cache_key)
        cache.set('homes_all_cache', sorted(set(homes_all_cache)))

    def get_category(self, category_slug):
        try:
            category = Taxonomy.objects.get(slug=category_slug, term__description='Categoria')
            return category
        except Taxonomy.DoesNotExist:
            return None

    def get_excludes(self):
        cache_key = self.cache_prefix % self.cache_key
        excludes = cache.get(cache_key, [])
        return excludes

    def set_excludes(self, excludes):
        cache_key = self.cache_prefix % self.cache_key
        cache.set(cache_key, sorted(set(excludes)), None)

    def get_articles_map(self):
        return []

    def get_articles_by_category(self, category_slug, quantity):

        excludes = self.get_excludes()

        category = self.get_category(category_slug)

        articles = Article.objects.filter(
            Q(
                feed__official=True,
                feed__content_type=article_type,
                publishin__lte=timezone.now(),
                feed__taxonomies__in=[category],
                status__in=[Article.STATUS_PUBLISH]
            )
        ).exclude(
            id__in=excludes
        ).order_by(
            '-publishin'
        )[0:quantity]

        for article in articles:
            excludes.append(article.pk)

        self.set_excludes(excludes)

        return articles

    def get_articles(self):

        articles = {}

        _map = self.get_articles_map()
        for category, quantity in _map:

            _articles = self.get_articles_by_category(category, quantity)
            articles.update({
                'category': _articles
            })

        return articles


class SiteHomePage(HomePageAbstract):

    def get_articles_map(self):
        return (
            ('design', 6),
            ('desenvolvimento', 4)
        )

    @property
    def cache_key(self):
        return 'home'
