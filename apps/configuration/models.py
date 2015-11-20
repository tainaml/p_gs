from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ConfigKey(models.Model):
    key = models.SlugField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)


class ConfigValues(models.Model):
    key = models.ForeignKey('ConfigKey', null=False, blank=False)
    value = models.TextField()
    object_id = models.PositiveIntegerField(null=False, blank=False)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')