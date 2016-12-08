# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth
from apps.core.business.content_types import ContentTypeCached
from apps.socialactions.models import Counter
from .manager import UserManager


def limit_usertypes_to(value):
    if value not in User.USER_TYPES.keys():
        raise ValidationError(
            _('This is not a valid user type'))

class User(AbstractUser):


    PERSON = 1
    ORGANIZATION = 2

    USER_TYPES = {
        PERSON: _("Person"),
        ORGANIZATION: _("Organization")
    }

    objects = UserManager()

    usertype = models.PositiveSmallIntegerField(verbose_name=_("User type"), validators=[limit_usertypes_to], default=PERSON)

    def is_company(self):
        return self.usertype == User.ORGANIZATION

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = u'Usuário'
        verbose_name_plural = u'Usuários'

    def get_full_name(self):
        return _('Anonymous') if not self.is_active else super(User, self).get_full_name()

    def get_short_name(self):
        return _('Anonymous') if not self.is_active else super(User, self).get_short_name()

    def get_absolute_ur(self):
        return 'javascript:void(0);' if not self.is_active else reverse('profile:show', args=[self.username])

    def get_absolute_url(self):
        return 'javascript:void(0);' if not self.is_active else reverse('profile:show', args=[self.username])

    @cached_property
    def user_profile(self):
        return self.profile if self.is_authenticated() else None

    @staticmethod
    def autocomplete_search_fields():
        return 'username', 'first_name', 'last_name'

    @cached_property
    def followers(self):
        try:
            return Counter.objects.defer("count").get(
                action_type=settings.SOCIAL_FOLLOW,
                object_id=self.id,
                content_type=ContentTypeCached.objects.get(model='user')

            ).count
        except:
            return 0

    @cached_property
    def is_social(self):
        return UserSocialAuth.objects.filter(user=self).exists()


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

        return self.is_valid()




