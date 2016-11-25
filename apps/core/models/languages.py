__author__ = 'phillip'

from django.db import models
from django.utils.translation import ugettext as _

class Language(models.Model):

    slug = models.SlugField(null=False, max_length=255, verbose_name=_('Slug'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    acronym = models.CharField(max_length=10, verbose_name=_('Acronym'))

    def __unicode__(self):
        return u'{}'.format(self.description)