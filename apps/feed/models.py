from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from apps.taxonomy.models import ObjectTaxonomy


class FeedObject(models.Model):

    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    obj_taxonomy = GenericRelation(ObjectTaxonomy, related_query_name="feed_obj")

    @property
    def date(self):
        return timezone.now()