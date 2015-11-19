from django.db import models


class Configkey(models.Model):
    key = models.SlugField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)


class Configvalues(models.Model):
    key = models.ForeignKey('config_key', null=False, blank=False)
    value = models.TextField()
    object_id = models.PositiveIntegerField(null=False, blank=False)
    content_object = models.GenericForeignKey('content_type', 'object_id', null=False, blank=False)