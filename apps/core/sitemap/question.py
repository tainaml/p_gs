from django.contrib.sitemaps import Sitemap
from apps.question.models import Question


class QuestionSitemap(Sitemap):

    limit = 10
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def lastmod(self, obj):
        return obj.question_date

    def items(self):

        items = Question.objects.filter(
            deleted=False
        )

        return items

    def location(self, obj):
        return obj.get_absolute_url()
