from django.utils.translation import ugettext as _

from apps.community.models import Community
from apps.core.models.tags import Tags
from apps.taxonomy.models import Taxonomy
from apps.geography.models import State, City
from apps.custom_base.service.custom import IdeiaForm, forms
from ..business import community as Business

__author__ = 'phillip'


class CoreCommunityFormSearch(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)
    taxonomies = forms.ModelMultipleChoiceField(queryset=Taxonomy.objects.all(), required=False)

    def __init__(self, items_per_page=None, *args, **kwargs):

        self.items_per_page = items_per_page
        super(CoreCommunityFormSearch, self).__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super(CoreCommunityFormSearch, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):

        return Business.get_communities(
            self.cleaned_data['taxonomies'],
            self.cleaned_data['criteria'],
            self.items_per_page,
            self.cleaned_data['page']
        )


class CoreCommunityFeedFormSearch(IdeiaForm):

    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)
    official = forms.BooleanField(required=False)

    def __init__(self, community_instance=None, content_types=None, itens_by_page=None, *args, **kwargs):
        self.community_instance=community_instance
        self.content_types = content_types
        self.itens_by_page = itens_by_page

        super(CoreCommunityFeedFormSearch, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreCommunityFeedFormSearch, self).clean()

        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        cleaned_data['official'] = cleaned_data.get('official', False)

        return cleaned_data

    def __process__(self):

        return Business.get_feed_objects(
            self.community_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.itens_by_page,
            self.cleaned_data['page'],
            self.cleaned_data.get('official')
        )


class CoreCommunityQuestionFeedFormSearch(CoreCommunityFeedFormSearch):

    replies = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(CoreCommunityQuestionFeedFormSearch, self).clean()

        cleaned_data['replies'] = cleaned_data['replies']\
            if 'replies' in cleaned_data and cleaned_data['replies'] else None

        return cleaned_data

    def __process__(self):

        return Business.get_feed_questions(
            self.community_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.cleaned_data['replies'],
            self.itens_by_page,
            self.cleaned_data['page']
        )


class CoreCommunitySearchVideosForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, community=None, items_per_page=10, *args, **kwargs):
        self.community = community
        self.items_per_page = items_per_page

        super(CoreCommunitySearchVideosForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreCommunitySearchVideosForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_articles_with_videos(
            self.community,
            self.cleaned_data.get('criteria'),
            self.items_per_page,
            self.cleaned_data.get('page', 1)
        )


class CoreCommunitySearchMaterialsForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)
    tags = forms.ModelChoiceField(queryset=Tags.objects.all().exclude(tag_slug="videos"), required=False,
                                  empty_label=_("All"))

    def __init__(self, community=None, items_per_page=10, *args, **kwargs):
        self.community = community
        self.items_per_page = items_per_page

        super(CoreCommunitySearchMaterialsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreCommunitySearchMaterialsForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_articles_with_tags(
            self.community,
            self.cleaned_data.get('criteria'),
            self.items_per_page,
            self.cleaned_data.get('page', 1),
            self.cleaned_data.get('tags')
        )


class CoreCommunityFollowersForm(IdeiaForm):

    community = forms.ModelChoiceField(queryset=Community.objects.all(), required=True)
    criteria = forms.CharField(required=False)
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, startswith=False, items_per_page=None, *args, **kwargs):
        self.startswith = startswith
        self.items_per_page = items_per_page

        super(CoreCommunityFollowersForm, self).__init__(*args, **kwargs)

        if self.data and 'state' in self.data and self.data.get('state'):
            self.fields['city'].queryset = City.objects.filter(state=self.data['state'])

    def clean(self):
        cleaned_data = super(CoreCommunityFollowersForm, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_followers(
            self.cleaned_data,
            self.items_per_page,
            self.cleaned_data.get('page'),
            self.startswith
        )