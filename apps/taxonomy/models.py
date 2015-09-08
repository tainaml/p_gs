from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Term(models.Model):
    description = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True)

class Taxonomy(models.Model):
    description = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True)
    term = models.ForeignKey(Term)

class ObjectTaxonomy(models.Model):
    taxonomy = models.ForeignKey(Taxonomy)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
