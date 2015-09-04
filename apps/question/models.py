from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):

    title = models.CharField(max_length=256, blank=False)
    description = models.CharField(min_length=200, max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    question_date = models.DateField(auto_now=False, auto_now_add=True, blank=False)
    correct_answer = models.OneToOneField(Answer)

class Answer(models.Model):

    description = models.CharField(min_length=200, max_length=2048, blank=False)
    author = models.ForeignKey(User, blank=False)
    answer_date = models.DateField(auto_now=False, auto_now_add=True, blank=False)