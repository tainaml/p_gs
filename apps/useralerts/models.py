from __future__ import unicode_literals
from django.db import models


class UserAlert(models.Model):

    title = models.CharField(max_length=150)
    content = models.TextField()