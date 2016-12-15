# -*- coding: utf-8 -*-
from django import forms
from apps.core.models.company import CompanyProxy
from apps.core.widgets.custom_field import ideia_custom_fielder


@ideia_custom_fielder()
class CompanyForm(forms.ModelForm):

    class Meta:

        model = CompanyProxy
        exclude = ('user', 'members')

        labels = {
            'name': u'Nome da Organização',
            'website': 'URL',
            'city': ''
        }

    members_formset = forms.inlineformset_factory(
        parent_model=CompanyProxy,
        model=CompanyProxy.members.through,
        exclude=(),
        extra=1
    )
