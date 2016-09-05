from django.db import transaction
from django.forms import CheckboxSelectMultiple
from reversion import revisions as reversion
from apps.article.service.forms import ArticleForm
from apps.feed.service import business as FeedBusiness
from apps.core.models.tags import Tags
from ..business import article as Business, tags as BusinessTags, feed as BusinessCoreFeed
from ..forms.taxonomies import CoreTaxonomiesMixin
from apps.custom_base.service.custom import forms
from apps.rede_gsti_signals.signals.home import clear_article_cache
from apps.core.business import user as UserBusiness


class CoreArticleBaseForm(ArticleForm, CoreTaxonomiesMixin):

    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all().order_by('tag_order'), required=False, widget=CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        self.instance = instance

        if instance:
            kwargs['initial'].update(self.get_feed_initial(instance))

        super(CoreArticleBaseForm, self).__init__(*args, **kwargs)

    def get_feed_initial(self, instance):
        feed_item = FeedBusiness.feed_get_or_create(instance)

        initial = {
            'tags': feed_item.tags.all(),
        }

        return initial

    def set_author(self, author):
        super(CoreArticleBaseForm, self).set_author(author)

        extra = None

        try:
            extra = self.instance.feed.all().first().communities.all()
        except Exception as e:
            print(e.message)
            pass


        self.filter_comunities(author, extra=extra)

    @transaction.atomic()
    @reversion.create_revision()
    def __process__(self):
        process_article = super(CoreArticleBaseForm, self).__process__()
        if process_article:
            reversion.set_user(process_article.author)
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)

        process_taxonomies = None

        if self.cleaned_data['communities']:
            process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)
        else:
            self.delete_taxonomies(process_feed, self.cleaned_data)
        process_tags = BusinessTags.save_feed_tags(process_feed, self.cleaned_data)

        #process_official = BusinessCoreFeed.save_feed_official(process_feed, self.cleaned_data)

        if process_feed:
            clear_article_cache.send(sender=process_feed.__class__, instance=process_feed)

        if self.cleaned_data['communities']:
            return process_article if (process_article and process_taxonomies and process_tags) else False
        else:
            return process_article if (process_article and process_tags) else False


class CoreArticleContributorForm(CoreArticleBaseForm):

    official = forms.BooleanField(required=False)

    def get_feed_initial(self, instance):
        initial = super(CoreArticleContributorForm, self).get_feed_initial(instance)
        feed_item = FeedBusiness.feed_get_or_create(instance)
        initial.update({
            'official': feed_item.official
        })
        return initial

    @transaction.atomic()
    @reversion.create_revision()
    def __process__(self):
        process_article = super(CoreArticleContributorForm, self).__process__()
        if not process_article:
            return False

        process_feed = process_article.feed.first()
        process_official = BusinessCoreFeed.save_feed_official(process_feed, self.cleaned_data)

        return process_article if process_official else False
