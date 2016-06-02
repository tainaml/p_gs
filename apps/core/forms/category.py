from django.core.exceptions import ValidationError
from apps.custom_base.service.custom import forms, IdeiaForm
import  apps.core.business.category as business
__author__ = 'phillip'


class ListArticleCommunityForm(IdeiaForm):

    category_id = forms.IntegerField(min_value=1, required=True)
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page
        super(ListArticleCommunityForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ListArticleCommunityForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):

        return business.get_articles_communities_by_category(
            self.cleaned_data['category_id'],
            self.itens_per_page,
            self.cleaned_data['page']
        )

