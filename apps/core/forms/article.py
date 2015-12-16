from django.db import transaction
from django.forms import CheckboxSelectMultiple

from apps.article.service.forms import ArticleForm
from apps.feed.service import business as FeedBusiness
from apps.core.models.tags import Tags
from ..business import article as Business, tags as BusinessTags, feed as BusinessCoreFeed
from ..forms.taxonomies import CoreTaxonomiesMixin
from custom_forms.custom import forms

class CoreArticleForm(ArticleForm, CoreTaxonomiesMixin):

    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all().order_by('tag_order'), required=False, widget=CheckboxSelectMultiple)
    official = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):

        kwargs['initial'] = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        if instance:
            feed_item = FeedBusiness.feed_get_or_create(instance)

            initial = {
                'tags': feed_item.tags.all(),
                'official': feed_item.official
            }

            kwargs['initial'].update(initial)

        super(CoreArticleForm, self).__init__(*args, **kwargs)


    def set_author(self, author):
        super(CoreArticleForm, self).set_author(author)
        self.filter_comunities(author)

    @transaction.atomic()
    def __process__(self):
        process_article = super(CoreArticleForm, self).__process__()
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)
        process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)
        process_tags = BusinessTags.save_feed_tags(process_feed, self.cleaned_data)
        process_official = BusinessCoreFeed.save_feed_official(process_feed, self.cleaned_data)

        return process_article if (process_article and process_taxonomies and process_tags and process_official) else False