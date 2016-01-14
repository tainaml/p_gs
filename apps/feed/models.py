from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models.tags import Tags
from apps.taxonomy.models import Taxonomy
from apps.community.models import Community


class FeedObject(models.Model):

    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)
    date = models.DateTimeField(null=True, auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    taxonomies = models.ManyToManyField(Taxonomy, related_name='feeds')
    communities = models.ManyToManyField(Community, related_name='feeds')
    tags = models.ManyToManyField(Tags, related_name='feeds')

    official = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return self.content_object