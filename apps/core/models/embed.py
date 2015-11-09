from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
import re


class EmbedItem(models.Model):

    TYPE_OTHER = 0
    TYPE_VIDEO = 1
    TYPE_SLIDES = 2

    TYPES_CHOICES = (
        (TYPE_VIDEO, 'Video'),
        (TYPE_SLIDES, 'Slides'),
        (TYPE_OTHER, 'Other'),
    )

    _TYPE_RULES = {
        TYPE_VIDEO: ur"^(http|https):\/\/(www\.)?(youtu.be|youtube|vimeo)(.com)?\/(watch\?[^#]*(v\=?)(\w+)|(\d+)).+$"
    }

    embed_type = models.IntegerField(choices=TYPES_CHOICES, null=False, default=TYPE_OTHER)
    embed_url = models.URLField(null=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def _define_type(self):
        for type, rule in self._TYPE_RULES.iteritems():
            p = re.compile(rule, re.IGNORECASE)
            if not re.match(p,str(self.embed_url)):
                continue

            self.embed_type = type
            return True

        # set type as "other" if not match in rules
        self.embed_type = self.TYPE_OTHER

    def save(self, *args, **kwargs):
        self._define_type()
        return super(EmbedItem, self).save(*args, **kwargs)