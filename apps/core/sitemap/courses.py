from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.core.models.course import Course


class CourseSitemap(Sitemap):

    limit = 10
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def lastmod(self, obj):
        return obj.updatein

    def items(self):

        items = Course.objects.filter(
            active=True
        )

        return items

    def location(self, obj):
        return reverse('course:show', args=(obj.slug,))