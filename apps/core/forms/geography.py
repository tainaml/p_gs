from apps.core.business.geography import get_geography
from apps.custom_base.service.custom import IdeiaForm, forms

class GeographyListForm(IdeiaForm):

    name = forms.CharField(required=False)
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, itens_per_page=10, model=None, *args, **kwargs):
        self.itens_per_page = itens_per_page
        self.model = model
        super(GeographyListForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(GeographyListForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):
        return  get_geography(
            self.model,
            self.cleaned_data['name'],
            self.itens_per_page,
            self.cleaned_data['page']
        )