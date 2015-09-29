from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from apps.taxonomy.models import Taxonomy
from apps.feed.models import FeedObject


class Answer(models.Model):

    description = models.TextField(max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    answer_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)
    question = models.ForeignKey("question.Question", related_name="question_owner", blank=False)


class Question(models.Model):

    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    question_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)
    correct_answer = models.OneToOneField("question.Answer", related_name="correct_answer", blank=True, null=True)
    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)
    feed = GenericRelation(FeedObject, related_query_name="question")
