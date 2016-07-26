from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from ckeditor.fields import RichTextField


class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author')
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    #content =  RichTextField()
    # content = models.CharField(max_length=settings.COMMENT_TEXT_LIMIT if hasattr(settings, "COMMENT_TEXT_LIMIT") else 10000, widget=CKEditorWidget(config_name='comment'))
    content = RichTextField(max_length=settings.COMMENT_TEXT_LIMIT if hasattr(settings, "COMMENT_TEXT_LIMIT") else 10000, default="comment")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    level = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return (self.content[:100] + "...") or "no content"

    @property
    def get_content_type(self):
        content = ContentType.objects.get_for_model(self)
        return content.model

