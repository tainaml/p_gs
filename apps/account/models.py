from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.


class MailValidation(models.Model):

    user = models.OneToOneField(User)
    token = models.TextField(unique=True)
    link_date = models.DateTimeField(default=timezone.now() + timedelta(days=2))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    def is_valid(self):
        return self.link_date <= timezone.now() + timedelta(days=2)
