from django.db import models
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Term(models.Model):
    description = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, blank=True, default="")
    parent = models.ForeignKey("self", null=True, blank=True)

    def __unicode__(self):
        return self.description


class Taxonomy(models.Model):
    description = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, blank=True, default="", db_index=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='taxonomies_children')
    term = models.ForeignKey(Term, related_name='taxonomies')

    update_in = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('description',)

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return self.slug if self.slug else '-'