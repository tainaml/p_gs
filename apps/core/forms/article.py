from django.core.exceptions import ValidationError
from apps.article.service.forms import ArticleForm

class CoreArticleForm(ArticleForm):

    def is_valid(self):

        valid = super(CoreArticleForm, self).is_valid()

        return valid