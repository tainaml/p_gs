from apps.core.utils import build_absolute_uri
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
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
    @cached_property
    def title(self):
        return self.question.title


class Question(models.Model):

    title = models.CharField(max_length=settings.QUESTION_TITLE_LIMIT if hasattr(settings, "QUESTION_TITLE_LIMIT") else 100, blank=False)
    slug = models.SlugField(default='', null=False, max_length=300)
    description = models.TextField(max_length=settings.QUESTION_TEXT_LIMIT if hasattr(settings, "QUESTION_TEXT_LIMIT") else 10000, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    question_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    correct_answer = models.OneToOneField("question.Answer", related_name="correct_answer", blank=True, null=True)
    deleted = models.BooleanField(default=False)

    VECTOR = SearchVector("question__title", weight="A") + SearchVector("question__description", weight="B")

    search_vector = SearchVectorField(null=True)

    feed = GenericRelation(FeedObject, related_query_name="question")

    comment_count = models.PositiveIntegerField(null=True, blank=True)
    like_count = models.PositiveIntegerField(null=True, blank=True)
    dislike_count = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        permissions = [
            ('change_other_questions', _('Can edit questions from others'))
        ]

    def check_is_owner(self, user):
        return self.author == user

    def counter_answer(self):
        return self.question_owner.count()

    def get_absolute_url(self):
        return reverse('question:show', args=[str(self.slug), str(self.id)])

    @cached_property
    def absolute_url(self):
        from django.core.urlresolvers import reverse
        path = reverse('question:show', args=[str(self.slug), str(self.id)])
        return build_absolute_uri(path)

    def __unicode__(self):
        return self.title + " - " + self.description[:100] + "..."