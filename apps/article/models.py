from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _


class Article(models.Model):

    STATUS_DRAFT = 0
    STATUS_TRASH = 2
    STATUS_PUBLISH = 4

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_TRASH, _('Trash')),
        (STATUS_PUBLISH, _('Publish'))
    )

    title = models.CharField(unique=True, default='', max_length=100)
    slug = models.SlugField(unique=True, default=slugify(title), max_length=150)
    text = models.TextField(unique=True, default='', max_length=2048)
    image = models.ImageField(max_length=100, upload_to='article/%Y/%m/%d')
    author = models.ForeignKey(User, related_name='articles', verbose_name=_('Author'))

    createdin = models.DateTimeField(null=False, auto_now_add=True)
    updatein = models.DateTimeField(null=False, auto_now=True)
    publishin = models.DateTimeField(null=True)

    status = models.IntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):

        return self.title
