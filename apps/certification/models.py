from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from apps.taxonomy.models import Taxonomy


class Certification(models.Model):

    title = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Title'))
    description = models.TextField(null=False, max_length=10000, verbose_name=_('Description'))

    slug = models.SlugField(null=False, blank=True, verbose_name=_('Slug'))
    about = models.TextField(null=True, blank=True, verbose_name=_('Sobre'))
    where_get = models.TextField(null=True, blank=True, verbose_name=_('Where get'))
    more_info = models.TextField(null=True, blank=True, verbose_name=_('More info'))
    taxonomies = models.ManyToManyField(to=Taxonomy, related_name='certifications', verbose_name=_('Related with'))

    active = models.BooleanField(default=False, verbose_name=_('Active'))

    def __unicode__(self):
        return self.title