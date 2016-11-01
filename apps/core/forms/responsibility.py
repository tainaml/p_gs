from apps.custom_base.service.custom import IdeiaForm
from apps.userprofile.models import Responsibility
from django import forms
from apps.taxonomy.service import business as TaxonomyBusiness


class ResponsibilityFiltersForm(IdeiaForm):

    page = forms.IntegerField(required=False)
    criteria = forms.CharField(required=False)
    category = forms.IntegerField(required=False)

    itens_per_page = 10

    def clean_page(self):
        page = self.cleaned_data.get('page', 1)
        return page

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category and TaxonomyBusiness.get_categories(list_ids=[category]).count() > 0:
            return category
        else:
            self.cleaned_data.pop('category')

    def __process__(self):
        qs = Responsibility.objects.all()
        page = self.cleaned_data.get('page')

        category = self.cleaned_data.get('category')
        if category:
            qs = qs.filter(categories__in=[category])

        criteria = self.cleaned_data.get('criteria')

        if criteria:
            qs = qs.filter(name__unaccent__icontains=criteria)

        return qs