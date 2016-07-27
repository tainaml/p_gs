from apps.custom_base.service.custom import IdeiaForm, forms
from apps.taxonomy.models import Taxonomy, Term
from ..business import search as Business


class SearchBaseForm(IdeiaForm):

    category = forms.CharField(required=False)
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
        if 'category' in self.cleaned_data and self.cleaned_data['category'] is not None and self.cleaned_data['category'] is not u'':
            return Business.get_communities(
                self.cleaned_data['q'],
                self.items_per_page,
                self.cleaned_data['page'],
                self.startswith,
                self.cleaned_data['category']
            )
        else:
            return Business.get_communities(
                self.cleaned_data['q'],
                self.items_per_page,
                self.cleaned_data['page'],
                self.startswith
            )


class SearchUserForm(SearchBaseForm):

    state = forms.IntegerField(required=False)
    city = forms.IntegerField(required=False)

    def __init__(self, items_per_page=None, startswith=False, *args, **kwargs):
        self.state = int(args[0]['state']) if "state" in args[0] else None
        self.city = int(args[0]['city']) if "city" in args[0] else None
        self.items_per_page = items_per_page
        self.startswith = startswith
        super(SearchBaseForm, self).__init__(*args, **kwargs)

    def __process__(self):
        return Business.get_users(
            self.cleaned_data['q'],
            self.items_per_page,
            self.cleaned_data['page'],
            self.startswith,
            self.state,
            self.city,
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
