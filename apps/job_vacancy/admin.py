# coding=utf-8
from django import forms
from django.contrib import admin

# Register your models here.
from apps.certification.models import Certification
from apps.company.models import Company
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


class JobVacancyAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'benefits',
    ]

    list_display = ('title', 'company', 'regime', 'home_office', 'quantity', 'workload', 'show_cargo')

    inlines = [
        JobVacancyLocationInLine,
        RequirementInLine,
        JobVacancyCertificationInLine,
        SalaryInLine,
        JobVacancyResponsibilityInLine,
    ]

    def show_cargo(self, obj):
        return "%s - %s" % (obj.resposibility.responsibility.name,
                            obj.resposibility.responsibility_type.description)

    show_cargo.short_description = "Cargo"

admin.site.register(Benefit)
admin.site.register(JobRegime)
admin.site.register(Level)
admin.site.register(Exigency)
admin.site.register(JobVacancyLocation)
admin.site.register(Certification)
admin.site.register(Company)
admin.site.register(Experience)
admin.site.register(SalaryType)
admin.site.register(WorkLoad)
admin.site.register(JobVacancyResponsibilityType)
admin.site.register(JobVacancy, JobVacancyAdmin)
