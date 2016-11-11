from django.core.management import BaseCommand
from django.conf import settings
from apps.article.models import Article
from apps.comment.models import Comment
from apps.core.business.content_types import ContentTypeCached
from apps.question.models import Question
from apps.socialactions.models import UserAction


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.filter(status=Article.STATUS_PUBLISH).order_by("id")

        content_type_article = ContentTypeCached.objects.get(model='article')

        print "Refreshing articles..."
        for article in articles:

            comment_count = Comment.objects.filter(content_type=content_type_article, object_id=article.id).count()
            article.comment_count = comment_count
            article.save()

        print "done"