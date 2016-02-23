# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ConfigGroup(models.Model):
    group = models.SlugField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)

    def __unicode__(self):
        return self.description


class ConfigKey(models.Model):
    key = models.SlugField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)
    group = models.ForeignKey(ConfigGroup, null=False, related_name='config_keys', verbose_name=_('Configs Keys'))
    show = models.BooleanField(null=False, blank=False, default=False)
    order = models.IntegerField(null=True, default=None)

    def __unicode__(self):
        return "%s (%s)" % self.description, self.key


class ConfigValues(models.Model):
    key = models.ForeignKey('ConfigKey', null=False, blank=False, related_name='config_values', verbose_name=_('Config Values'))
    value = models.TextField(null=False, blank=False)
    object_id = models.PositiveIntegerField(null=False, blank=False)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s: %s" % self.key.key, self.value