from django.core.exceptions import ValidationError
from django.db import transaction
from apps.article.service.forms import ArticleForm, forms
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from ..business import article as Business


class TaxonomiesChoiceField(forms.ModelMultipleChoiceField):

    def clean(self, value):

        values = []

        try:

            tax_objects = []
            values = str(value[0]).split(',')

        except Exception, e:
            print e.message

        return super(TaxonomiesChoiceField, self).clean(values)

    def validate(self, value):
        print 'Validate:'
        print value
        return super(TaxonomiesChoiceField, self).validate(value)


class CoreArticleForm(ArticleForm):

    taxonomies = forms.ModelMultipleChoiceField(required=False, queryset=Taxonomy.objects.all(),)
    communities = TaxonomiesChoiceField(required=True, queryset=Community.objects.all(),)


    @transaction.atomic()
    def __process__(self):
        process_article = super(CoreArticleForm, self).__process__()
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)
        process_core = Business.save_taxonomies(process_feed, self.cleaned_data)

        return process_article if (process_article and process_core) else False