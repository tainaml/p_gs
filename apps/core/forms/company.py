# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from apps.core.models.company import CompanyProxy, Membership
from apps.taxonomy.models import Taxonomy
from apps.core.widgets.custom_field import (
    ideia_custom_fielder, ideia_field_wraper,
    CustomFielderWidget
)


class TaxonomyModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return u'{}'.format(obj.description)


@ideia_custom_fielder()
class CompanyForm(forms.ModelForm):

    categories = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_categories(),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'hidden'})
    )

    communities = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_communities(),
        widget=widgets.SelectMultiple(attrs={'class': 'shows'})
    )

    def __init__(self, *args, **kwargs):

        instance = kwargs.get('instance')
        if instance:

            initial = kwargs.get('initial', {})
            initial.update({
                'categories': instance.taxonomies.filter(term__slug='categoria'),
                'communities': instance.taxonomies.filter(term__slug='comunidade')
            })

            kwargs.update({
                'initial': initial
            })

        super(CompanyForm, self).__init__(*args, **kwargs)

    class Meta:

        model = CompanyProxy
        exclude = ('user', 'members', 'taxonomies')
        labels = {
            'name': u'Nome da Organização',
            'website': 'URL',
            'city': ''
        }

    def save(self, commit=True):
        super(CompanyForm, self).save(commit)

        for tax in self.cleaned_data.get('categories', []):
            self.instance.taxonomies.add(tax)

        for tax in self.cleaned_data.get('communities', []):
            self.instance.taxonomies.add(tax)
