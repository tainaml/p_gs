from django.core.management import BaseCommand
from django.conf import settings
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.socialactions.models import UserAction


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.filter(status=Article.STATUS_PUBLISH).order_by("id")

        content_type_article = ContentTypeCached.objects.get(model='article')
        for article in articles:


            comment_count = UserAction.objects.filter(object_id=article.id,
                                          content_type=content_type_article,
                                          action_type=settings.SOCIAL_COMMENT).count()

            article.comment_count=comment_count
            like_count = UserAction.objects.filter(object_id=article.id,
                                          content_type=content_type_article,
                                          action_type=settings.SOCIAL_LIKE).count()


            article.like_count=like_count
            dislike_count = UserAction.objects.filter(object_id=article.id,
                                          content_type=content_type_article,
                                          action_type=settings.SOCIAL_UNLIKE).count()


            article.dislike_count=dislike_count
            article.save()