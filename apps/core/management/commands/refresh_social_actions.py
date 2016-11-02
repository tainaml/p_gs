from django.core.management import BaseCommand
from django.conf import settings
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.question.models import Question
from apps.socialactions.models import UserAction


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.filter(status=Article.STATUS_PUBLISH).order_by("id")

        content_type_article = ContentTypeCached.objects.get(model='article')
        content_type_question = ContentTypeCached.objects.get(model='question')

        print "Refreshing articles..."
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

        questions = Question.objects.all()
        print "Refreshing questions..."
        for question in questions:
            answer_count = UserAction.objects.filter(object_id=question.id,
                                          content_type=content_type_question,
                                          action_type=settings.SOCIAL_ANSWER).count()

            question.comment_count=answer_count
            like_count = UserAction.objects.filter(object_id=question.id,
                                          content_type=content_type_question,
                                          action_type=settings.SOCIAL_LIKE).count()


            question.like_count=like_count
            dislike_count = UserAction.objects.filter(object_id=question.id,
                                          content_type=content_type_question,
                                          action_type=settings.SOCIAL_UNLIKE).count()


            question.dislike_count=dislike_count
            question.save()

        print "done"