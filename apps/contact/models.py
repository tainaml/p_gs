from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):

    # case user aren't member of social network
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    # case user are member of social network
    author = models.ForeignKey(User, blank=True, null=True)

    subject = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=1024, blank=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)


