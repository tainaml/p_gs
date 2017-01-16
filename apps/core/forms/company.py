# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import widgets, BaseFormSet, BaseInlineFormSet
from apps.company.models import Company
from apps.core.models.company import CompanyProxy, Membership
from apps.custom_base.service.custom import MaterialModelForm
from django.utils.translation import ugettext as _

class TaxonomyModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return u'{}'.format(obj.description)

def verify_if_exists(value):
    User = get_user_model()
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            _('This e-mail already exists!'))

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

    email = forms.EmailField(required=True, label=_("Email"), validators=[verify_if_exists])

    request_user = None

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
        
    def save(self, commit=True):
        self.instance.user.email = self.cleaned_data['email']
        instance = super(CompanyForm, self).save(commit=commit)

        return instance

