from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.conf import settings

class User(AbstractUser):
    pass

class TokenType():
    REGISTER_ACCOUNT_CONFIRM = 1
    RECOVERY_PASSWORD_CONFIRM = 2

    TIME = {
        'REGISTER_ACCOUNT': 48,
        'TIME_RECOVERY_PASSWORD': 8
    }


class MailValidation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.TextField(unique=True)
    link_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    token_type = models.IntegerField()

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

        if self.token_type == TokenType.REGISTER_ACCOUNT_CONFIRM:
            time = settings.TIME_REGISTER_ACCOUNT if settings.TIME_REGISTER_ACCOUNT else \
                TokenType.TIME['REGISTER_ACCOUNT']
            return self.link_date + timedelta(hours=time) >= timezone.now()

        elif self.token_type == TokenType.RECOVERY_PASSWORD_CONFIRM:
            time = settings.TIME_RECOVERY_PASSWORD if settings.TIME_RECOVERY_PASSWORD else \
                TokenType.TIME['TIME_RECOVERY_PASSWORD']
            return self.link_date + timedelta(hours=time) >= timezone.now()

    def is_active(self):
        """
        Method checks if token is active
        :return: Boolean
        """

        return self.active


