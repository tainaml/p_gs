# -*- coding: utf-8 -*-
from django import forms
from apps.core.models.company import CompanyProxy, Membership
from apps.core.widgets.custom_field import (
    ideia_custom_fielder, ideia_field_wraper,
    CustomFielderWidget
)


@ideia_custom_fielder()
class CompanyCustomModelForm(forms.ModelForm):

    class Meta:
        model = CompanyProxy.members.through
        exclude = ()

def ideia_formfield_cb(field):
    new_field = ideia_field_wraper(field)
    return new_field.formfield()


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
        form=CompanyCustomModelForm,
        exclude=(),
        widgets={
            'user': CustomFielderWidget.factory(forms.widgets.Select, label=u'Usuário LOL')
        },
        extra=1,
    )
