from django import forms

from apps.custom_base.service.custom import IdeiaForm
from . import business as Business


class JobSearchForm(IdeiaForm):

    keywords = forms.CharField(required=False)
    locale = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.items_per_page = None
        super(JobSearchForm, self).__init__(*args, **kwargs)

    def set_items_per_page(self, qnt=10):
        self.items_per_page = qnt

    def clean(self):
        cleaned_data = super(JobSearchForm, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_jobs(
            keyowrs=self.cleaned_data.get('keywords'),
            locale=self.cleaned_data.get('locale'),
            items_per_page=self.items_per_page,
            page=self.cleaned_data.get('page')
        )
