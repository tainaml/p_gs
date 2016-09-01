from django.core.management import BaseCommand
from apps.article.models import Article
from reversion import revisions as reversion

class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.filter(first_slug='')

        for article in articles:
            version_list = reversion.get_for_object(article).get_unique()
            slug_list = [version.field_dict['slug'] for version in version_list]
            if slug_list:
                slug = slug_list[-1]
                article.first_slug = slug
                article.save()