from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.article.models import Article
from apps.community.models import Community
from django.db.models import Q
from apps.feed.models import FeedObject

__author__ = 'phillip'

# TODO Move this repetition to custom_base for reuse
def get_articles_communities_by_category(category_id=None, items_per_page=None, page=None):

    communities = Community.objects.filter(taxonomy__parent__id=category_id)

    feed_objects = FeedObject.objects.filter(
        Q(article__status=Article.STATUS_PUBLISH)
        # & Q(communities__in=communities)

    )

    items_per_page = items_per_page if items_per_page else 10

    paginated_article_communities = Paginator(feed_objects, items_per_page)

    try:
        paginated_article_communities = paginated_article_communities.page(page)
    except PageNotAnInteger:
        paginated_article_communities = paginated_article_communities.page(1)
    except EmptyPage:
        paginated_article_communities = []

    return paginated_article_communities