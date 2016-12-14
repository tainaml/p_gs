from django.utils.translation import ugettext as _
from django import forms
from django.db import models
from apps.job_vacancy.models import (
    JobVacancy, JobVacancyResponsibility,
    Responsibility, JobVacancyResponsibilityType,
    JobVacancyLocation,
    Salary
)


class JobVacancyForm(forms.ModelForm):

    # # Responsibility Fields
    # responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.filter(active=True), required=True)
    # responsibility_type = forms.ModelChoiceField(queryset=JobVacancyResponsibilityType.objects.all(), required=True)

    responsibility_formset = forms.inlineformset_factory(
        parent_model=JobVacancy,
        model=JobVacancyResponsibility,
        exclude=(),
        extra=1,
        max_num=1
    )

    location_formset = forms.inlineformset_factory(
        parent_model=JobVacancy,
        model=JobVacancyLocation,
        exclude=(),
        extra=1
    )

    salary_formset = forms.inlineformset_factory(
        parent_model=JobVacancy,
        model=Salary,
        exclude=(),
        extra=1,
        max_num=1
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

    def save(self, commit=True):

        item = super(JobVacancyForm, self).save(commit)
        job_responsibility, created = JobVacancyResponsibility.objects.get_or_create(
            responsibility=self.cleaned_data.get('responsibility'),
            responsibility_type=self.cleaned_data.get('responsibility_type'),
            job_vacancy=item
        )
        job_responsibility.save()
        return item
