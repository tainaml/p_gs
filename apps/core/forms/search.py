from custom_forms.custom import IdeiaForm, forms
from ..business import search as Business


class SearchBaseForm(IdeiaForm):

    q = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, items_per_page=None, startswith=False, *args, **kwargs):
        self.items_per_page = items_per_page
        self.startswith = startswith
        super(SearchBaseForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SearchBaseForm, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


class SearchCommunityForm(SearchBaseForm):
    def __process__(self):
        return Business.get_communities(
            self.cleaned_data['q'],
            self.items_per_page,
            self.cleaned_data['page'],
            self.startswith
        )


class SearchUserForm(SearchBaseForm):
    def __process__(self):
        return Business.get_users(
            self.cleaned_data['q'],
            self.items_per_page,
            self.cleaned_data['page'],
            self.startswith
        )


class SearchArticleForm(SearchBaseForm):
    def __process__(self):
        return Business.get_articles(
            self.cleaned_data['q'],
            self.items_per_page,
            self.cleaned_data['page']
        )


class SearchQuestionForm(SearchBaseForm):
    def __process__(self):
        return Business.get_questions(
            self.cleaned_data['q'],
            self.items_per_page,
            self.cleaned_data['page']
        )