__author__ = 'phillip'
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

class Rating(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='ratings',
                               verbose_name=_('Author'))

    value = models.PositiveIntegerField()
