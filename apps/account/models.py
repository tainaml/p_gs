from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
from django.utils import timezone


class MailValidation(models.Model):

    user = models.OneToOneField(User)
    token = models.TextField(unique=True)
    link_date = models.DateTimeField(default=datetime.today())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    def is_valid(self):
        """
        date_created = 2015-08-24 (+2days)
        date_expire  = 2015-08-26
        ---------------------------

        fake_today   = 2015-08-24

        condition = date_create + 2 days >= fake_today

        :return:
        """
        return self.link_date + timedelta(days=2) >= timezone.now()
