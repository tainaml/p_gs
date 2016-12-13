from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db import models
from apps.certification.models import Certification
from apps.company.models import Company
from apps.geography.models import City, State, Country
from apps.taxonomy.models import Taxonomy
from apps.userprofile.models import Responsibility
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey
from social.utils import slugify


class JobRegime(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class Benefit(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class WorkLoad(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class JobVacancy(models.Model):
    title = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(default='', null=False, max_length=150, verbose_name=_('Slug'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))
    job_vacancy_date = models.DateField(default=timezone.now, null=False, verbose_name=_('Date'))
    company = models.ForeignKey(Company, null=True, blank=True, related_name='job_vacancys', verbose_name=_('Company'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='job_vacancys',
                               verbose_name=_('Author'))
    job_vacancy_responsibility = models.TextField(null=True, blank=True, max_length=10000,
                                                  verbose_name=_('Responsibility Description'))
    regime = models.ForeignKey(JobRegime, blank=True, null=True, verbose_name=_('Regime'))
    home_office = models.BooleanField(verbose_name=_('Home Office'), default=False, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Quantity'))
    workload = models.ForeignKey(WorkLoad, null=True, blank=True, verbose_name=_('Work Load'))
    benefits = models.ManyToManyField(Benefit, blank=True, verbose_name=_('Benefits'))
    email = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('E-mail'))
    phone_number = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Phone Number'))
    site = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Web Site'))
    contact = models.TextField(null=True, blank=True, max_length=10000, verbose_name=_('Contact'))

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.slug:
            self.slug = slugify(self.title)

        super(JobVacancy, self).save(force_insert, force_update, using, update_fields)


class JobVacancyAdditionalRequirement(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, null=False, related_name='additional_requirements', on_delete=models.CASCADE,
                                    blank=False, verbose_name=_('Job Vacancy'))

    description = models.CharField(blank=False, null=False, max_length=512, verbose_name=_('Aditional Requirement'))

class JobVacancyLocation(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, null=False, related_name='locations', on_delete=models.CASCADE,
                                    blank=False, verbose_name=_('Job Vacancy'))
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, verbose_name=_('States'), null=True, blank=True)
    cities = ChainedManyToManyField(City, chained_field="state", chained_model_field="state", verbose_name=_('Cities'), null=True, blank=True)


class SalaryType(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class Salary(models.Model):
    fixed_value = models.FloatField(null=True, blank=True, verbose_name=_('Fixed value'))
    range_value_from = models.FloatField(null=True, blank=True, verbose_name=_('Range from'))
    range_value_to = models.FloatField(null=True, blank=True, verbose_name=_('Range to'))
    regime = models.ForeignKey(SalaryType, null=False, verbose_name=_('Salary Type'))
    job_vacancy = models.OneToOneField(JobVacancy, on_delete=models.CASCADE, related_name='salary', primary_key=True,
                                       verbose_name=_('Job Vacancy'))


class JobVacancyResponsibilityType(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class JobVacancyResponsibility(models.Model):
    responsibility = models.ForeignKey(Responsibility, null=True, verbose_name=_('Responsibility'))
    responsibility_type = models.ForeignKey(JobVacancyResponsibilityType, null=True, blank=True,
                                            verbose_name=_('Responsibility Type'))
    job_vacancy = models.OneToOneField(JobVacancy, on_delete=models.CASCADE, related_name='responsibility',
                                       primary_key=True, verbose_name=_('Job Vacancy'))


class Level(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class Exigency(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class Experience(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class Requirement(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='requirements', null=False,
                                    verbose_name=_('Job Vacancy'))
    item = models.ForeignKey(Taxonomy, null=False, blank=False, verbose_name=_('Item'))
    level = models.ForeignKey(Level, null=True, blank=True, verbose_name=_('Level'))
    exigency = models.ForeignKey(Exigency, null=True, blank=True,  verbose_name=_('Exigency'))
    experience = models.ForeignKey(Experience, null=True, blank=True,  verbose_name=_('Experience'))


class JobVacancyCertification(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='certifications', null=False,
                                    verbose_name=_('Job Vacancy'))
    certification = models.ForeignKey(Certification, null=False, verbose_name=_('Certification'))
    exigency = models.ForeignKey(Exigency, null=False, verbose_name=_('Exigency'))
