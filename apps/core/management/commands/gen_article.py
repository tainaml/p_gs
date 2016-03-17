from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.article.models import Article
from apps.feed.models import FeedObject
from apps.community.models import Community
from apps.core.business.feed import save_taxonomies


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        article_type = ContentType.objects.get_for_model(Article)

        feeds = FeedObject.objects.filter(
            content_type=article_type,
        )

        community = Community.objects.filter(slug='cobit')
        listing = list(community)

        for feed in feeds:
            article = feed.article.first()
            if not article:
                continue

            feed.communities.add(*listing)
            feed.date = timezone.now()

            save_taxonomies(feed)

            feed.save()
            article.publishin = timezone.now()
            article.status = Article.STATUS_PUBLISH
            article_saved = article.save()