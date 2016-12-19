# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from apps.core.models.company import CompanyProxy, Membership
from apps.core.widgets.custom_field import (
    ideia_custom_fielder, ideia_field_wraper,
    CustomFielderWidget
)


class TaxonomyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return u'{}'.format(obj.description)


@ideia_custom_fielder()
class CompanyForm(forms.ModelForm):

    categories = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_categories(),
        empty_label=None,
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'hidden'})
    )

    communities = TaxonomyModelChoiceField(
        queryset=CompanyProxy.list_communities(),
        empty_label=None,
        widget=widgets.SelectMultiple
    )

    class Meta:

        model = CompanyProxy
        exclude = ('user', 'members', 'taxonomies')
        labels = {
            'name': u'Nome da Organização',
            'website': 'URL',
            'city': ''
        }

    members_formset = forms.inlineformset_factory(
        parent_model=CompanyProxy,
        model=CompanyProxy.members.through,
        exclude=(),
        can_delete=False,
        widgets={
            'user': widgets.HiddenInput,
            'permission': widgets.HiddenInput
        },
        extra=1,
    )
