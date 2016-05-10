# coding=utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse
# Register your models here.

from django import forms
from apps.certification.models import Certification
from apps.job_vacancy.models import Requirement, JobVacancyCertification, Salary, JobVacancy, Benefit, \
    JobRegime, Level, Exigency, Experience, SalaryType, JobVacancyResponsibility, WorkLoad, JobVacancyResponsibilityType, \
    JobVacancyLocation


class RequirementInLine(admin.TabularInline):
    model = Requirement


class JobVacancyCertificationInLine(admin.TabularInline):
    model = JobVacancyCertification


class JobVacancyLocationInLine(admin.TabularInline):
    model = JobVacancyLocation


class SalaryInLine(admin.TabularInline):
    model = Salary


class JobVacancyResponsibilityInLine(admin.TabularInline):
    model = JobVacancyResponsibility


class JobVacancyAdminForm(forms.ModelForm):

    class Meta:
        model = JobVacancy
        fields = '__all__'

class JobVacancyAdmin(admin.ModelAdmin):
    form = JobVacancyAdminForm
    filter_horizontal = [
        'benefits',
    ]

    list_display = ('title', 'show_salary', 'show_cargo', 'company', 'regime', 'workload', 'quantity', 'home_office')

    def view_on_site(self, obj):

        return reverse('jobs:detail', args=[obj.slug, obj.id])

    inlines = [
        JobVacancyLocationInLine,
        RequirementInLine,
        JobVacancyCertificationInLine,
        SalaryInLine,
        JobVacancyResponsibilityInLine,
    ]

    def show_salary(self, obj):
        if obj.salary.regime.description == "Valor fixo":
            return "R$ %.2f" % obj.salary.fixed_value
        elif obj.salary.regime.description == "Intervalo":
            return "R$ %.2f - R$ %.2f" % (obj.salary.range_value_from,
                                          obj.salary.range_value_to)
        else:
            return obj.salary.regime.description

    show_salary.short_description = "Salário"

    def show_cargo(self, obj):
        return "%s - %s" % (obj.resposibility.responsibility_type.description,
                            obj.resposibility.responsibility.name)

    show_cargo.short_description = "Cargo"

admin.site.register(Benefit)
admin.site.register(JobRegime)
admin.site.register(Level)
admin.site.register(Exigency)
admin.site.register(JobVacancyLocation)
admin.site.register(Certification)
admin.site.register(Experience)
admin.site.register(SalaryType)
admin.site.register(WorkLoad)
admin.site.register(JobVacancyResponsibilityType)
admin.site.register(JobVacancy, JobVacancyAdmin)
