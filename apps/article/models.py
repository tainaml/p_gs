from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextField
from django.conf import settings
from apps.core.models.embed import EmbedItem
from apps.feed.models import FeedObject


class Article(models.Model):

    STATUS_TEMP = 1
    STATUS_TRASH = 2
    STATUS_DRAFT = 3
    STATUS_PUBLISH = 4

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_TRASH, _('Trash')),
        (STATUS_PUBLISH, _('Publish'))
    )

    title = models.CharField(blank=False, null=False,
                             max_length=settings.ARTICLE_TITLE_LIMIT if hasattr(settings, "ARTICLE_TITLE_LIMIT") else 100)
    slug = models.SlugField(default='', null=False, max_length=150)
    text = RichTextField(null=False, max_length=settings.ARTICLE_TEXT_LIMIT if hasattr(settings, "ARTICLE_TEXT_LIMIT") else 10000)
    image = models.ImageField(max_length=100, upload_to='article/%Y/%m/%d', blank=True, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='articles', verbose_name=_('Author'))

    createdin = models.DateTimeField(null=False, auto_now_add=True)
    updatein = models.DateTimeField(null=False, auto_now=True)
    publishin = models.DateTimeField(null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, null=False)

    feed = GenericRelation(FeedObject, related_query_name="article")
    embed = GenericRelation(EmbedItem, related_query_name="article")

    def is_published(self):
        return self.status == self.STATUS_PUBLISH

    def get_image(self):
        return self.image if self.image else None

    def do_publish(self, update_date=False):
        pub = self.publishin
        if not self.publishin:
            self.publishin = timezone.now()

        if update_date:
            self.publishin = update_date if isinstance(update_date, timezone.datetime) else timezone.now()

        self.status = self.STATUS_PUBLISH

    def do_save(self):
        if not self.status:
            self.status = self.STATUS_DRAFT

        if self.status == self.STATUS_PUBLISH and not self.publishin:
            self.publishin = timezone.now()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article:view', args=[str(self.id), str(self.slug)])

    def __unicode__(self):
        return self.title or "no title"