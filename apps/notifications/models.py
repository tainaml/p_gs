from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.db import models


class Notification(models.Model):

    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_received')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_sent')

    #Target
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')

    notification_date = models.DateTimeField(auto_now=True)
    notification_action = models.PositiveIntegerField(choices=[(k, v) for k, v, in settings.NOTIFICATION_ACTIONS.items()])

    read = models.BooleanField(null=False, blank=False, default=False)
    visualized = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        app_label = "notifications"


@python_2_unicode_compatible
class Alert(models.Model):

    INFO = 1
    DANGER = 2
    WARNING = 3
    SUCCESS = 4

    ALERT_CHOICES = (
        (INFO, _('Info')),
        (DANGER, _('Danger')),
        (WARNING, _('Warning')),
        (SUCCESS, _('Success')),
    )

    title = models.CharField(null=False, blank=False, max_length=150)
    message = models.TextField(null=False, blank=False)

    type = models.IntegerField(choices=ALERT_CHOICES, null=False)

    updated_in = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Updated In"))
    created_in = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Created In"))

    def __str__(self):
        return self.title
