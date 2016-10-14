from django.db.models import QuerySet
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from apps.custom_base.service.custom import forms, IdeiaModelForm
from apps.feed.service import business as FeedBusiness
from ..business import user as UserBusiness
from ..business import feed as CoreFeedBusiness


class CoreTaxonomiesMixin(IdeiaModelForm):

    taxonomies = forms.ModelMultipleChoiceField(required=False, queryset=Taxonomy.objects.all(),)
    communities = forms.ModelMultipleChoiceField(required=False, queryset=Community.objects.all(),)

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        if instance is not None:
            self.__load_other_fields(instance, kwargs)

        # Load article communities and update the initial data
        super(CoreTaxonomiesMixin, self).__init__(*args, **kwargs)

    def __load_other_fields(self, instance, kwargs):
        feed_item = FeedBusiness.feed_get_or_create(instance)

        initial = {
            'communities': feed_item.communities.all(),
            'taxonomies': feed_item.taxonomies.all()
        }

        kwargs['initial'].update(initial)

    def filter_comunities(self, author, extra=None):
        communities = self.fields.get('communities')

        if extra is None:
            try:
                extra = self.instance.feed.all().first().communities.all()
            except Exception as e:
                pass

        if communities:
            _user_communities = UserBusiness.get_user_communities(author)
            communities.queryset = _user_communities
            if extra is not None and isinstance(extra, (QuerySet)):
                communities.queryset = communities.queryset | extra

    def save_taxonomies(self, target_object, form_data):
        process_communities = CoreFeedBusiness.save_communities(target_object, self.cleaned_data)
        process_core = CoreFeedBusiness.save_taxonomies(target_object, self.cleaned_data)
        return process_communities and process_core

    def delete_taxonomies(self, target_object, form_data):
        CoreFeedBusiness.delete_taxonomies(target_object, self.cleaned_data)
        CoreFeedBusiness.delete_communities(target_object, self.cleaned_data)
