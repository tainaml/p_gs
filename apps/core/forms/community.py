from custom_forms.custom import IdeiaForm, forms
from ..business import community as Business

__author__ = 'phillip'


class CoreCommunityFormSearch(IdeiaForm):
    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, community_instance=None, content_types=None, itens_by_page=None, *args, **kwargs):
        self.community_instance=community_instance
        self.content_types = content_types
        self.itens_by_page = itens_by_page

        super(CoreCommunityFormSearch, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(CoreCommunityFormSearch, self).clean()

        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):

        return Business.get_feed_objects(
            self.community_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.itens_by_page,
            self.cleaned_data['page']
        )
