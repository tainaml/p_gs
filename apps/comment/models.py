from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# Create your models here.

class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author')
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    content = models.CharField(max_length=512)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    level = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return (self.content[:100] + "...") or "no content"


