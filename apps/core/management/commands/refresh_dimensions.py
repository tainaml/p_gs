from django.core.management import BaseCommand
from apps.article.models import Article

class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.all()

        for article in articles:
            if article.image:
                article.image_width = article.image.width
                article.image_height = article.image.height
                print "Setting for '%s'" % article.title
                article.save()


