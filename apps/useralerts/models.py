from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class UserAlert(models.Model):

    STATUS_DRAFT = 1
    STATUS_PUBLISH = 2
    STATUS_SENDED = 3

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISH, 'Publish'),
        (STATUS_SENDED, 'Sended')
    )

    title = models.CharField(max_length=150)
    content = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)

    def is_published(self):
        return bool(self.status == self.STATUS_PUBLISH)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('useralerts:show', args=[self.id])