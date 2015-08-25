from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta


class MailValidation(models.Model):

    user = models.OneToOneField(User)
    token = models.TextField(unique=True)
    link_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    def is_valid(self):
        """
        Method checks if token is valid

        Example
        date_created = 2015-08-24 (+2days)
        date_expire  = 2015-08-26
        ---------------------------

        fake_today   = 2015-08-25

        if date_create + 2 days >= fake_today:
            return True
        else:
            return False

        :return: Boolean
        """
        return self.link_date + timedelta(days=2) >= timezone.now()

    def is_active(self):
        """
        Method checks if token is active
        :return: Boolean
        """

        return self.active