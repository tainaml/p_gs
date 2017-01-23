from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext as _
from django import forms
from django.db import models
from apps.custom_base.service.custom import MaterialModelForm
from apps.custom_base.widgets.material import CheckboxSelectMultipleMaterial, InputTextMaterial, MaterialSelectMultiple
from apps.geography.models import City, State
from apps.job_vacancy.models import (
    JobVacancy, JobVacancyResponsibility,
    Responsibility, JobVacancyResponsibilityType,
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





class JobVacancyForm(MaterialModelForm):

    use_required_attribute = False

    states = forms.ModelMultipleChoiceField(queryset=State.objects.none(), required=False)
    cities = forms.ModelMultipleChoiceField(queryset=City.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(JobVacancyForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['states']._set_queryset(self.instance.states)
            self.fields['cities']._set_queryset(self.instance.cities)


    responsibility_formset = forms.inlineformset_factory(
        form=MaterialModelForm,
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


    def full_clean(self):



        super(JobVacancyForm, self).full_clean()

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
