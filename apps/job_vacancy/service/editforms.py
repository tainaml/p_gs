from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext as _
from django import forms
from apps.custom_base.service.custom import MaterialModelForm
from apps.custom_base.widgets.material import CheckboxSelectMultipleMaterial, InputTextMaterial
from apps.geography.models import City, State
from apps.job_vacancy.models import (
    JobVacancy, JobVacancyResponsibility,
    Salary,
    Requirement, JobVacancyAdditionalRequirement)


class SalaryFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
         super(SalaryFormSet, self).add_fields(form, index)
         #TODO refactor to a better aproach
         form.fields["fixed_value"] = forms.FloatField(localize=True, widget=InputTextMaterial, required=False)
         form.fields["fixed_value"].widget.label = _('Fixed value')



         form.fields["range_value_from"] = forms.FloatField(localize=True, widget=InputTextMaterial, required=False)
         form.fields["range_value_from"].widget.label = _('Range from')

         form.fields["range_value_to"] = forms.FloatField(localize=True, widget=InputTextMaterial, required=False)
         form.fields["range_value_to"].widget.label = _('Range to')


class ResposibilityForm(MaterialModelForm):
    detached_responsibility = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput)

    class Meta:
        model = JobVacancyResponsibility
        fields = ('responsibility', 'responsibility_type')

# class ResponsibilityFormset(BaseInlineFormSet):
#
#     def clean(self):
#
#         super(ResponsibilityFormset, self).clean()
#         print self.forms[0].cleaned_data

class JobVacancyForm(MaterialModelForm):

    use_required_attribute = False

    states = forms.ModelMultipleChoiceField(queryset=State.objects.all().prefetch_related("country"), required=False)
    cities = forms.ModelMultipleChoiceField(queryset=City.objects.all().prefetch_related("state", "state__country"), required=False)


    #TODO find a better way to don't get all cities
    def clean(self):

        self.fields['states'].queryset = State.objects.all().prefetch_related("country")
        self.fields['cities'].queryset = City.objects.all().prefetch_related("state", "state__country")
        super(JobVacancyForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(JobVacancyForm, self).__init__(*args, **kwargs)

        self.fields["cities"].widget.label = _('Cities related with the job vacancy')
        self.fields["states"].widget.label = _('State related with the job vacancy')

        if self.instance.pk:
            self.fields['states']._set_queryset(self.instance.states)
            self.fields['cities']._set_queryset(self.instance.cities)


    responsibility_formset = forms.inlineformset_factory(
        form=ResposibilityForm,
        formset=BaseInlineFormSet,
        labels=None,
        parent_model=JobVacancy,
        model=JobVacancyResponsibility,
        exclude=(),
        extra=1,
        max_num=1,
        min_num=1,
        validate_max=True,
        validate_min=True
    )


    salary_formset = forms.inlineformset_factory(
        labels=None,
        formset=SalaryFormSet,
         form=MaterialModelForm,
        parent_model=JobVacancy,
        model=Salary,
        exclude=(),
        extra=1,
        max_num=1,
        min_num=1,
        validate_max=True,
        validate_min=True
    )

    requirements_formset = forms.inlineformset_factory(
        labels=None,
         form=MaterialModelForm,
        parent_model=JobVacancy,
        model=Requirement,
        exclude=(),
        extra=0,
        min_num=1,
    )
    aditional_requirements_formset = forms.inlineformset_factory(
        labels=None,
         form=MaterialModelForm,
        parent_model=JobVacancy,
        model=JobVacancyAdditionalRequirement,
        exclude=(),
        extra=0,
        min_num=1,
    )


    class Meta:

        model = JobVacancy
        fields = [
            'title', 'quantity', 'job_vacancy_responsibility', 'states','cities',
            'email', 'phone_number', 'site',
            'company', 'home_office',
            'regime', 'workload',
            'benefits', 'observation'
        ]

        widgets =  {
            'benefits':CheckboxSelectMultipleMaterial
        }

    def set_author(self, author):
        if self.instance:
            self.instance.author = author
