from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def get_content_type(model=None):
    try:
        return ContentType.objects.get(model=model)
    except ContentType.DoesNotExist:
        return None


AVAIABLE_TYPES_TO_RATE = [get_content_type(model)
                          for model in getattr(settings, "AVAIABLE_TYPES_TO_RATE", ['course']) if get_content_type(model)]

def content_in_settings(value):
    try:
        content_type = ContentType.objects.get(id=value)

    except ContentType.DoesNotExist:
        raise ValidationError(
            _('Type is not registered to rate!')
        )

    if content_type not in AVAIABLE_TYPES_TO_RATE:
        raise ValidationError(
            _('Type is not registered to rate!')
        )



def max_float(value):
    MAX_RATING = getattr(settings, 'MAX_RATING', 5.00)
    if value > getattr(settings, 'MAX_RATING', 5.00):
        raise ValidationError(
            _('value is larger than maximum %(value)s'), params={'value': MAX_RATING},
        )

class Rating(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='ratings',
                               verbose_name=_('Author'))

    MAX_RATING = getattr(settings, 'MAX_RATING', 5.00)
    value = models.DecimalField(max_digits=3, decimal_places=2, validators=[max_float])
    rating_date = models.DateTimeField(default=timezone.now, null=False, verbose_name=_('Date'))
    comment = models.TextField(blank=True, null=True, max_length=1024)


    class Meta:
        unique_together = (("content_type", "object_id", "author"),)

    #ContentType
    content_type = models.ForeignKey(ContentType, validators=[content_in_settings])
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
