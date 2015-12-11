from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from custom_forms.custom import forms, IdeiaForm, IdeiaModelForm
from apps.feed.service import business as FeedBusiness
from ..business import user as UserBusiness
from ..business import feed as CoreFeedBusiness


class CoreTaxonomiesMixin(IdeiaModelForm):

    taxonomies = forms.ModelMultipleChoiceField(required=False, queryset=Taxonomy.objects.all(),)
    communities = forms.ModelMultipleChoiceField(required=True, queryset=Community.objects.all(),)

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

    def filter_comunities(self, author):
        communities = self.fields.get('communities')
        if communities:
            communities.queryset = UserBusiness.get_user_communities(author)

    def save_taxonomies(self, target_object, form_data):
        process_communities = CoreFeedBusiness.save_communities(target_object, self.cleaned_data)
        process_core = CoreFeedBusiness.save_taxonomies(target_object, self.cleaned_data)
        return (process_communities and process_core)