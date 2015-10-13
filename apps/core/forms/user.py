from django.db import transaction
from custom_forms.custom import IdeiaForm, forms
from ..business import user as Business

from apps.userprofile.models import Responsibility, State
from apps.userprofile.service import business as BusinessUserProfile
from apps.userprofile.service.forms import EditProfileForm


class CoreUserSearchForm(IdeiaForm):
    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, profile_instance=None, content_types=None, itens_by_page=None, *args, **kwargs):
        self.profile_instance=profile_instance
        self.content_types = content_types
        self.itens_by_page = itens_by_page

        super(CoreUserSearchForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(CoreUserSearchForm, self).clean()

        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):

        return Business.get_feed_objects(
            self.profile_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.itens_by_page,
            self.cleaned_data['page']
        )


class CoreUserProfileEditForm(EditProfileForm):

    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.all())
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1))


    @transaction.atomic()
    def __process__(self):
        process_profile = super(CoreUserProfileEditForm, self).__process__()
        process_occupation = BusinessUserProfile.create_occupation(process_profile, data={
            'responsibility': self.cleaned_data['responsibility']
        })

        return process_profile if (process_profile and process_occupation) else False