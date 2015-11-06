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
            values = str(value[0]).split(',')
        except Exception, e:
            print e.message

        return super(TaxonomiesChoiceField, self).clean(values)


class CoreArticleForm(ArticleForm):

    taxonomies = forms.ModelMultipleChoiceField(required=False, queryset=Taxonomy.objects.all(),)
    communities = TaxonomiesChoiceField(required=True, queryset=Community.objects.all(),)

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        if instance is not None:
            self.load_other_fields(instance, kwargs)

        # Load article communities and update the initial data
        super(CoreArticleForm, self).__init__(*args, **kwargs)

    def load_other_fields(self, instance, kwargs):
        feed_item = Business.BusinessFeed.feed_get_or_create(instance)

        initial = {
            'communities': feed_item.communities.all(),
            'taxonomies': feed_item.taxonomies.all()
        }

        kwargs['initial'].update(initial)


    @transaction.atomic()
    def __process__(self):
        process_article = super(CoreArticleForm, self).__process__()
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)
        process_communities = Business.save_communities(process_feed, self.cleaned_data)
        process_core = Business.save_taxonomies(process_feed, self.cleaned_data)

        return process_article if (process_article and process_communities and process_core) else False