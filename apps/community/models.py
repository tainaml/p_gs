from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from apps.socialactions.models import UserAction
from apps.taxonomy.models import Taxonomy

class Community(models.Model):

    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.SlugField(blank=False, null=False, max_length=150)
    description = models.TextField(null=False, max_length=2048)
    image = models.ImageField(max_length=100, upload_to='community/%Y/%m/%d', blank=True, default='')
    taxonomy = models.OneToOneField(Taxonomy, related_name="community_related")
    user_action = GenericRelation(UserAction, related_query_name="community")

    def __unicode__(self):
        return self.title

    def get_picture(self):
        return self.image if self.image else None