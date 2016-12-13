from django import forms
from django.db import models
from apps.job_vacancy.models import (
    JobVacancy, JobVacancyResponsibility,
    Responsibility, JobVacancyResponsibilityType
)


class JobVacancyForm(forms.ModelForm):

    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.filter(active=True), required=True)
    responsibility_type = forms.ModelChoiceField(queryset=JobVacancyResponsibilityType.objects.all(), required=True)

    class Meta:

        model = JobVacancy
        fields = [
            'title', 'quantity', 'job_vacancy_responsibility',
            'email', 'phone_number', 'site'
        ]

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
