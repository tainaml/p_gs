from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.community.models import Community


class ComplaintType(models.Model):

    description = models.TextField(null=False, max_length=256)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.description


class Complaint(models.Model):
    description = models.TextField(null=True, max_length=512)
    complaint_type = models.ForeignKey(ComplaintType)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    communities = models.ManyToManyField(Community)

    def __unicode__(self):
        return self.complaint_type.description