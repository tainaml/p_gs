from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from apps.taxonomy.models import Taxonomy
from apps.feed.models import FeedObject


class Answer(models.Model):

    description = RichTextField(max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    answer_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)
    question = models.ForeignKey("question.Question", related_name="question_owner", blank=False)


class Question(models.Model):

    title = models.CharField(max_length=256, blank=False)
    slug = models.SlugField(default='', null=False, max_length=300)
    description = RichTextField(max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    question_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)
    correct_answer = models.OneToOneField("question.Answer", related_name="correct_answer", blank=True, null=True)
    feed = GenericRelation(FeedObject, related_query_name="question")

    def counter_answer(self):
        return self.question_owner.count()
