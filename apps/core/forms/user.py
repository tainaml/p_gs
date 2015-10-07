from custom_forms.custom import IdeiaForm, forms
from ..business import user as Business


class CoreUserSearchForm(IdeiaForm):

    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, profile_instance=None, content_types=None,
        itens_by_page=None, user=None, *args, **kwargs):

        self.profile_instance=profile_instance
        self.content_types = content_types
        self.itens_by_page = itens_by_page
        self.user = user

        super(CoreUserSearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreUserSearchForm, self).clean()

        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):

        return Business.get_feed_objects(
            self.profile_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.itens_by_page,
            self.cleaned_data['page'],
            self.user
        )


class CoreUserProfileForm(CoreUserSearchForm):

    def __process__(self):

        return Business.get_articles_from_user(
            profile_instance=self.profile_instance,
            description=self.cleaned_data['criterio'],
            content_type=self.content_types,
            items_per_page=self.itens_by_page,
            page=self.cleaned_data['page']
        )