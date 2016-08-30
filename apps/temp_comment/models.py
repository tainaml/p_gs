from __future__ import unicode_literals

from django.db import models
from ..article.models import Article


class TempComment(models.Model):

    author = models.CharField(max_length=255)

    article = models.ForeignKey(Article, null=True)

    google_id = models.CharField(max_length=512)
    parent_google_id = models.CharField(max_length=512)

    creation_date = models.DateTimeField()

    text = models.TextField()