from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

AVAIABLE_TYPES_TO_RATE = [ContentType.objects.get(model=model)
                          for model in getattr(settings, "AVAIABLE_TYPES_TO_RATE", ['course'])]

def content_in_settings(value):
    try:
        content_type = ContentType.objects.get(id=value)

    except ContentType.DoesNotExist:
        raise ValidationError(
            _('Type is not registered to rate!')
        )

    if content_type not in AVAIABLE_TYPES_TO_RATE:
        print content_type
        raise ValidationError(
            _('Type is not registered to rate!')
        )


MAX_RATING = 5.00
def max_float(value):
    if value > MAX_RATING:
        raise ValidationError(
            _('value is larger than maximum %(value)s'), params={'value': MAX_RATING},
        )

class Rating(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='ratings',
                               verbose_name=_('Author'))

    value = models.DecimalField(max_digits=3, decimal_places=2, validators=[max_float])
    rating_date = models.DateTimeField(default=timezone.now, null=False, verbose_name=_('Date'))
    comment = models.TextField(blank=True, null=True, max_length=1024)


    class Meta:
        unique_together = (("content_type", "object_id", "author"),)

    #ContentType
    content_type = models.ForeignKey(ContentType, validators=[content_in_settings])
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
