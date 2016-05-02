from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models


class Company(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Name'))
    logo = models.ImageField(max_length=100, upload_to='company/%Y/%m/%d', blank=True, default='', verbose_name=_('Logo'))

    def __unicode__(self):
        return self.name

    def get_logo(self):
        return self.logo if self.logo else None
