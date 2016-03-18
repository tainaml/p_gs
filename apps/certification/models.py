from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

# Create your models here.

class Certification(models.Model):

    title = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Title'))
    description = models.TextField(null=False, max_length=10000, verbose_name=_('Description'))

    def __unicode__(self):
        return self.title