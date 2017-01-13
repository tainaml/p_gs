# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets, BaseFormSet, BaseInlineFormSet
from apps.company.models import Company
from apps.core.models.company import CompanyProxy, Membership
from apps.custom_base.service.custom import MaterialModelForm
from apps.custom_base.widgets.material import InputTextMaterial
from apps.taxonomy.models import Taxonomy
from apps.core.widgets.custom_field import (
    ideia_custom_fielder, ideia_field_wraper,
    CustomFielderWidget
)


class TaxonomyModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return u'{}'.format(obj.description)


class CompanyForm(MaterialModelForm):

    use_required_attribute = False

    categories = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_categories(),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'hidden'})
    )

    communities = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_communities(),
        widget=widgets.SelectMultiple(attrs={'class': 'shows'})
    )

    request_user = None

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
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



    class Meta:

        model = CompanyProxy
        exclude = ('user', 'taxonomies', 'members')
        labels = {
            'name': u'Nome da Organização',
            'website': 'URL',
            'city': 'Cidade'
        }
        widgets = {
            "logo": forms.FileInput
            # "name": InputTextMaterial
        }

    def set_request_user(self, user):
        self.request_user = user

