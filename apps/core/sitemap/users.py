from apps.article.models import Article
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from apps.userprofile.models import UserProfile
from django.urls import reverse


class UserSitemap(Sitemap):

    limit = 10
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def lastmod(self, obj):
        return obj.updatein if obj and hasattr(obj, "updatein") else obj.user.date_joined

    def items(self):

        items = UserProfile.objects.all().filter(
            wizard_step=getattr(settings, 'WIZARD_STEPS_TOTAL', 3),
            user__is_active=True,
            user__articles__status=Article.STATUS_PUBLISH
        ).prefetch_related('user').distinct()

        return items

    def location(self, obj):
        return reverse('profile:show', args=(obj.user.username,))
