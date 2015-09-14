from django.db import models
from django.contrib.auth.models import User


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