from __future__ import absolute_import
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.db import models

from apps.core.business.content_types import ContentTypeCached
from apps.socialactions.models import UserAction, Counter
from apps.taxonomy.models import Taxonomy


class Community(models.Model):

    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.SlugField(blank=False, null=False, max_length=150, db_index=True)
    description = models.TextField(null=False)
    image = models.ImageField(max_length=100, upload_to='community/%Y/%m/%d', blank=True)
    relevance = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0)

    related = models.ManyToManyField("self",
                                     blank=True,
                                     related_name="related_community",
                                     symmetrical=False,
                                     verbose_name=_("Community Related"))

    taxonomy = models.OneToOneField(Taxonomy, related_name="community_related")
    user_action = GenericRelation(UserAction, related_query_name="community")

    update_in = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_picture(self):
        return self.image if self.image else None

    #User Action Follower
    @cached_property
    def followers(self):
        try:
            return Counter.objects.defer("count").get(
                action_type=settings.SOCIAL_FOLLOW,
                object_id=self.id,
                content_type=ContentTypeCached.objects.get(model='community')

            ).count
        except:
            return 0



