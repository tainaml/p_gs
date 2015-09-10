from django.core.exceptions import ValidationError
from django.db import transaction
from apps.article.service.forms import ArticleForm, forms
from apps.taxonomy.models import Taxonomy
from ..business import article as Business


class CoreArticleForm(ArticleForm):

    taxonomies = forms.ModelMultipleChoiceField(queryset=Taxonomy.objects.all()
                                                , required=True)

    def is_valid(self):

        valid = super(CoreArticleForm, self).is_valid()

        return valid

    @transaction.atomic()
    def process(self):
        process_article = super(CoreArticleForm, self).process()
        process_core = Business.save_taxonomies(self.instance, self.cleaned_data)

        return process_article and process_core
