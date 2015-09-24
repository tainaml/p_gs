from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext as _

from apps.taxonomy.models import ObjectTaxonomy


class Article(models.Model):

    STATUS_DRAFT = 0
    STATUS_TEMP = 1
    STATUS_TRASH = 2
    STATUS_PUBLISH = 4

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_TRASH, _('Trash')),
        (STATUS_PUBLISH, _('Publish'))
    )

    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.SlugField(default='', null=False, max_length=150)
    text = models.TextField(null=False, max_length=2048)
    image = models.ImageField(max_length=100, upload_to='article/%Y/%m/%d', blank=True, default='')
    author = models.ForeignKey(User, null=False, related_name='articles', verbose_name=_('Author'))
    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)

    createdin = models.DateTimeField(null=False, auto_now_add=True)
    updatein = models.DateTimeField(null=False, auto_now=True)
    publishin = models.DateTimeField(null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, null=False)

    obj_taxonomy = GenericRelation(ObjectTaxonomy, related_query_name='articles')



    def is_published(self):
        return self.status == self.STATUS_PUBLISH


    def __unicode__(self):
        return self.title

    def get_image(self):
        return self.image if self.image else None
