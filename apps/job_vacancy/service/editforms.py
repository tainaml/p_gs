from django.utils.translation import ugettext as _
from django import forms
from django.db import models
from apps.custom_base.service.custom import MaterialModelForm
from apps.job_vacancy.models import (
    JobVacancy, JobVacancyResponsibility,
    Responsibility, JobVacancyResponsibilityType,
    JobVacancyLocation,
    Salary,
    Requirement, JobVacancyAdditionalRequirement)


class JobVacancyForm(MaterialModelForm):

    # # Responsibility Fields
    # responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.filter(active=True), required=True)
    # responsibility_type = forms.ModelChoiceField(queryset=JobVacancyResponsibilityType.objects.all(), required=True)

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

    location_formset = forms.inlineformset_factory(
        labels=None,
        form=MaterialModelForm,
        parent_model=JobVacancy,
        model=JobVacancyLocation,
        exclude=(),
        extra=1
    )

    salary_formset = forms.inlineformset_factory(
        labels=None,
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
            'title', 'quantity', 'job_vacancy_responsibility',
            'email', 'phone_number', 'site',
            'company', 'home_office',
            'regime', 'workload',
            'benefits', 'observation'
        ]

        widgets =  {
            'benefits': forms.CheckboxSelectMultiple
        }

    def set_author(self, author):
        if self.instance:
            self.instance.author = author
