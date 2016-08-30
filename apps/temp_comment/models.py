from __future__ import unicode_literals

from django.db import models

class TempComment(models.Model):

    author = models.CharField(max_length=255)

    google_id = models.CharField(max_length=512)
    parent_google_id = models.CharField(max_length=512)

    creation_date = models.DateTimeField()

    text = models.TextField()