from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class UserAction(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='action_author')
    action_date = models.DateTimeField(auto_now=True)
    action_type = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='target_user', null=True)


class Counter(models.Model):

    action_type = models.PositiveIntegerField()

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='target_user_counter', null=True)
    count = models.PositiveIntegerField()
