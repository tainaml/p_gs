from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings
from apps.taxonomy.models import Taxonomy


def limit_to_membershiptypes(value):
    if value not in Membership.MEMBERSHIP_TYPES.keys():
        raise ValidationError(
            _('This is not a valid membership'))

class Membership(models.Model):

    ADMIN = 1
    COLLABORATOR = 2

    MEMBERSHIP_TYPES = {
        ADMIN: _("Admin"),
        COLLABORATOR: _("Collaborator")
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    company = models.ForeignKey("Company", on_delete=models.CASCADE, verbose_name=_("Company"))

    permission = models.PositiveSmallIntegerField(verbose_name=_("Permission"), validators=[limit_to_membershiptypes])

class CompanyManager(models.Manager):
    def get_queryset(self):
        return super(CompanyManager, self).get_queryset().select_related('user', 'user__profile')

class Company(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name=_('Name'))
    logo = models.ImageField(max_length=100, upload_to='company/%Y/%m/%d', blank=True, verbose_name=_('Logo'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='company', blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Membership", related_name="companies")
    description = models.TextField(blank=False, null=False, verbose_name=_('Description'))

    objects = CompanyManager()

    website = models.URLField(verbose_name=_('Website'), blank=True, null=True)


    taxonomies = models.ManyToManyField(Taxonomy, verbose_name=_("Taxonomies"), related_name="companies")

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