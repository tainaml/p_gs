from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from apps.core.business.content_types import ContentTypeCached

from apps.taxonomy.models import Taxonomy
from apps.feed.models import FeedObject


class Answer(models.Model):

    description = models.TextField(max_length=settings.ANSWER_TEXT_LIMIT if hasattr(settings, "ANSWER_TEXT_LIMIT") else 10000, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)
    answer_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)
    question = models.ForeignKey("question.Question", related_name="question_owner", blank=False)

    def __unicode__(self):
        return self.description[:100] + "..."

    @property
    def get_content_type(self):
        content = ContentTypeCached.objects.get(model="answer")
        return content.model


class Question(models.Model):

    title = models.CharField(max_length=settings.QUESTION_TITLE_LIMIT if hasattr(settings, "QUESTION_TITLE_LIMIT") else 100, blank=False)
    slug = models.SlugField(default='', null=False, max_length=300)
    description = models.TextField(max_length=settings.QUESTION_TEXT_LIMIT if hasattr(settings, "QUESTION_TEXT_LIMIT") else 10000, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    question_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    correct_answer = models.OneToOneField("question.Answer", related_name="correct_answer", blank=True, null=True)
    deleted = models.BooleanField(default=False)

    feed = GenericRelation(FeedObject, related_query_name="question")

    def check_is_owner(self, user):
        return self.author == user

    def counter_answer(self):
        return self.question_owner.count()

    def get_absolute_url(self):
        return reverse('question:show', args=[str(self.slug), str(self.id)])

    def __unicode__(self):
        return self.title + " - " + self.description[:100] + "..."