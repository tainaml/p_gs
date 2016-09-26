from django.contrib.sitemaps import Sitemap
from apps.article.models import Article
from django.urls import reverse


class BaseArticleSitemap(Sitemap):

    limit = 100
    changefreq = "daily"
    __priority = 0.5

    def lastmod(self, obj):
        return obj.updatein

    def priority(self, obj):
        return self.__priority

    def items(self):

        items = Article.objects.filter(
            status=Article.STATUS_PUBLISH,
        )

        return items

    def location(self, obj):
        return obj.get_absolute_url()


class ArticleSitemap(BaseArticleSitemap):

    def items(self):
        return super(ArticleSitemap, self).items().filter(
            feed__official=False
        )


class ArticleOfficialSitemap(BaseArticleSitemap):

    __priority = 0.8

    def items(self):
        return super(ArticleOfficialSitemap, self).items().filter(
            feed__official=True
        )
