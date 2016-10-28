from django.contrib.sitemaps import Sitemap
from apps.taxonomy.models import Taxonomy
from django.urls import reverse


class CategorySitemap(Sitemap):

    limit = 10
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def lastmod(self, obj):
        return obj.update_in

    def items(self):

        items = Taxonomy.objects.filter(
            term__description='Categoria'
        )

        return items

    def location(self, obj):
        return reverse('category:show', args=(obj.slug,))