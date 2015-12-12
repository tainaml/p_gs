from django.db import transaction

from apps.article.service.forms import ArticleForm
from ..business import article as Business
from ..forms.taxonomies import CoreTaxonomiesMixin


class CoreArticleForm(ArticleForm, CoreTaxonomiesMixin):


    def set_author(self, author):
        super(CoreArticleForm, self).set_author(author)
        self.filter_comunities(author)

    @transaction.atomic()
    def __process__(self):
        process_article = super(CoreArticleForm, self).__process__()
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)
        process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)

        return process_article if (process_article and process_taxonomies) else False