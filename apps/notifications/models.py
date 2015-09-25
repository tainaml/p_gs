from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.utils import timezone


class Notification(models.Model):

    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_received')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_sent')

    #Target
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')

    notification_date = models.DateTimeField(auto_now=True)
    notification_action = models.PositiveIntegerField()

    class Meta:
        app_label = "notifications"





