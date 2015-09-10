from django.core.exceptions import ValidationError
from apps.article.service.forms import ArticleForm, IdeiaModelForm
from apps.taxonomy.models import ObjectTaxonomy

class CoreArticleCategoriesForm(IdeiaModelForm):

    class Meta:
        model = ObjectTaxonomy
        exclude = []


    def is_valid(self):
        valid = super(CoreArticleCategoriesForm, self).is_valid()

        return valid


class CoreArticleForm(ArticleForm):

    def is_valid(self):

        valid = super(CoreArticleForm, self).is_valid()
        return valid