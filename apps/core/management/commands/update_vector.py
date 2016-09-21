from django.contrib.postgres.search import SearchVector
from django.core.management import BaseCommand
from apps.article.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.filter(status=Article.STATUS_PUBLISH)
        vector = SearchVector("title", weight="A") + SearchVector("text", weight="B")

        for article in articles:
            article.search_vector = vector
            article.save()
            print "saving %s" % article.slug

