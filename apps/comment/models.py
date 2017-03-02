from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.functional import cached_property

from apps.core.business.content_types import ContentTypeCached

COMMENT_CONTENT_TYPE = ContentTypeCached.objects.get(model='comment')

class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author')
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    content = models.TextField(max_length=settings.COMMENT_TEXT_LIMIT if hasattr(settings, "COMMENT_TEXT_LIMIT") else 10000, default="comment")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    level = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return (self.content[:100] + "...") or "no content"

    @property
    def get_content_type(self):
        content = ContentTypeCached.objects.get(model="comment")
        return content.model

    @cached_property
    def get_root_object(self):
        print self.id, self.content_object
        if self.content_type == COMMENT_CONTENT_TYPE:

            return self.content_object.get_root_object()
        else:
            return self.content_object





