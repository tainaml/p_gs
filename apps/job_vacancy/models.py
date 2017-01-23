# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
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
    active = models.BooleanField(default=False, verbose_name=_('Active'))

    def __unicode__(self):
        return self.description


class WorkLoad(models.Model):
    description = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Description'))

    def __unicode__(self):
        return self.description


class JobVacancy(models.Model):
    title = models.CharField(blank=False, null=False, max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(default='', null=False, max_length=150, verbose_name=_('Slug'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    job_vacancy_date = models.DateField(default=timezone.now, null=False, verbose_name=_('Date'))
    company = models.ForeignKey(Company, null=True, blank=True, related_name='job_vacancys', verbose_name=_('Company'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='job_vacancys',
                               verbose_name=_('Author'))
    job_vacancy_responsibility = models.TextField(null=True, blank=True, max_length=10000,
                                                  verbose_name=_('Responsibility Description'))
    regime = models.ForeignKey(JobRegime, blank=True, null=True, verbose_name=_('Regime'))
    home_office = models.BooleanField(verbose_name=_('Home Office'), default=False, blank=True)
    quantity = models.IntegerField(null=True, blank=True, verbose_name=_('Quantity'), validators=[MinValueValidator(1, message=_("Only number greater than 1 are permitted"))])
    workload = models.ForeignKey(WorkLoad, null=True, blank=True, verbose_name=_('Work Load'))
    benefits = models.ManyToManyField(Benefit, blank=True, verbose_name=_('Benefits'))
    email = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('E-mail'))
    phone_number = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Phone Number'))
    site = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Web Site'))
    contact = models.TextField(null=True, blank=True, max_length=10000, verbose_name=_('Contact'))
    observation = models.TextField(null=True, blank=True, max_length=10000,
                                                  verbose_name=_('Observation'))

    cities = models.ManyToManyField(City, blank=True, verbose_name=_('Cities'))
    states = models.ManyToManyField(State, blank=True, verbose_name=_('States'))


    def can_modify(self, user=None):
        return ( user and (user.is_superuser or self.author == user))

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

class Salary(models.Model):

    TYPE_INTERVAL = 1
    TYPE_FIXED = 2
    TYPE_COMBINE = 3

    CHOICES_TYPE = (
        (TYPE_INTERVAL, _('Interval')),
        (TYPE_FIXED, _('Fixed')),
        (TYPE_COMBINE, _('Combine'))
    )

    fixed_value = models.FloatField(null=True, blank=True, verbose_name=_('Fixed value'))
    range_value_from = models.FloatField(null=True, blank=True, verbose_name=_('Range from'))
    range_value_to = models.FloatField(null=True, blank=True, verbose_name=_('Range to'))
    salary_type = models.PositiveIntegerField(choices=CHOICES_TYPE, default=TYPE_COMBINE, verbose_name=_('Type'))
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

    def clean(self):
        if ((self.level or self.exigency) and not self.item) or (self.exigency and not self.level):
            raise ValidationError(_("Um item deve ser associado se for selecionado um nível ou uma exigência"))

    item = models.ForeignKey(Taxonomy, null=True, blank=True, verbose_name=_('Item'))
    level = models.ForeignKey(Level, null=True, blank=True, verbose_name=_('Level'))
    exigency = models.ForeignKey(Exigency, null=True, blank=True,  verbose_name=_('Exigency'))
    experience = models.ForeignKey(Experience, null=True, blank=True,  verbose_name=_('Experience'))


class JobVacancyCertification(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='certifications', null=False,
                                    verbose_name=_('Job Vacancy'))
    certification = models.ForeignKey(Certification, null=False, verbose_name=_('Certification'))
    exigency = models.ForeignKey(Exigency, null=False, verbose_name=_('Exigency'))
