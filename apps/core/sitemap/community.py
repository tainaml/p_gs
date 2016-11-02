from django.contrib.sitemaps import Sitemap
from apps.community.models import Community
from django.urls import reverse


class CommunitySitemap(Sitemap):

    limit = 10
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def lastmod(self, obj):
        return obj.update_in

    def items(self):
        items = Community.objects.all()
        return items

    def location(self, obj):
        return reverse('community:show', args=(obj.slug,))