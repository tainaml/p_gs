from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models


class Company(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Name'))
    logo = models.ImageField(max_length=100, upload_to='company/%Y/%m/%d', blank=True, default='', verbose_name=_('Logo'))

    description = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Description'))

    def __unicode__(self):
        return self.name

    def get_logo(self):
        return self.logo if self.logo else None


class CompanyContactType(models.Model):
    description = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class CompanyContact(models.Model):
    description = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Description'))
    type = models.ForeignKey(to=CompanyContactType, blank=False, null=False, verbose_name=_('Type'))
    company = models.ForeignKey(to=Company, blank=False, null=False, verbose_name=_('Company'))