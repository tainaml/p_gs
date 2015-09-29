from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Term(models.Model):
    description = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True)

    def __unicode__(self):
        return self.description

class Taxonomy(models.Model):
    description = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='taxonomies')
    term = models.ForeignKey(Term, related_name='taxonomies')

    def __unicode__(self):
        return self.description