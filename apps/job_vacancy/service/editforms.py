from django.db.models import Q
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
from apps.userprofile.models import Responsibility


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

    author = None

    detached_responsibility = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput)
    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.filter(Q(avaiable_to_choose=True) | Q(author=author)), required=False)

    def clean(self):
        cleaned_data = super(ResposibilityForm, self).clean()

        return cleaned_data

    class Meta:
        model = JobVacancyResponsibility
        fields = ('responsibility', 'responsibility_type')




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
            
    def is_valid(self):
        self_valid = super(JobVacancyForm, self).is_valid()
        responsibility_formset_valid = self.responsibility_formset.is_valid()
        salary_formset_valid =  self.salary_formset.is_valid()
        requirements_formset_valid = self.requirements_formset.is_valid()
        aditional_requirements_formset_valid = self.aditional_requirements_formset.is_valid()

        return self_valid and responsibility_formset_valid and salary_formset_valid \
               and requirements_formset_valid and aditional_requirements_formset_valid


    def save(self, commit=True):
        instance = super(JobVacancyForm, self).save(commit)

        responsibility_form = self.responsibility_formset.forms[0]
        self.responsibility_formset.save()
        if 'detached_responsibility' in responsibility_form.cleaned_data \
            and responsibility_form.cleaned_data['detached_responsibility'] != '' \
            and not responsibility_form.cleaned_data['responsibility']:
            name = responsibility_form.cleaned_data['detached_responsibility']
            new_responsibility = Responsibility(name=name, avaiable_to_choose=False)
            new_responsibility.save()
            instance.responsibility.responsibility = new_responsibility
            instance.save()


        self.salary_formset.save()

        self.requirements_formset.save()
        self.aditional_requirements_formset.save()

        return instance
