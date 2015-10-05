from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextField


class GenderType:
    def __init__(self):
        pass

    MALE = 'M'
    FEMALE = 'F'

    LABEL = {
        MALE: _("MALE"),
        FEMALE: _("FEMALE")
    }


class Country(models.Model):
    name = models.CharField(max_length=60, blank=False)
    abbreviation = models.CharField(max_length=3, blank=False)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=60, blank=False)
    abbreviation = models.CharField(max_length=3, blank=False)
    country = models.ForeignKey(Country, related_name='states')

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60, blank=False)
    state = models.ForeignKey(State, related_name='cities')

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    profile_picture = models.ImageField(max_length=100, upload_to='userprofile/%Y/%m/%d', blank=True, default='')
    wizard_step = models.IntegerField(null=False, blank=False, default=0)

    def __unicode__(self):
        return self.user

    def has_locale(self):
        if self.city and self.city.state and self.city.state.country:
            return True
        return False

    def locale(self):
        if self.has_locale():
            return "%s - %s - %s" % (self.city.name.title(),
                                     self.city.state.abbreviation.upper(),
                                     self.city.state.country.name.title())
        return ""

    @property
    def age(self):
        if hasattr(self, "property_age") and self.property_age:
            return self.property_age

        if self.birth:
            born = self.birth
            today = date.today()

            # return int(round((date.today() - self.birth).days / 365.2425, 3))
            self.property_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return self.property_age

        return False

    @property
    def current_occupation(self):
        if hasattr(self, "property_current_occupation") and self.property_current_occupation:
            return self.property_current_occupation

        if self.occupation.count():
            self.property_current_occupation = self.occupation.order_by('-id')[:1][0]
            return self.property_current_occupation

        return False

    @property
    def occupations(self):
        if hasattr(self, "property_occupations") and self.property_occupations:
            return self.property_occupations

        if self.occupation.count():
            self.property_occupations = self.occupation.order_by('-id')
            return self.property_occupations

        return False

    def get_profile_picture(self):
        return self.profile_picture if self.profile_picture else None


class Responsibility(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    text = RichTextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Occupation(models.Model):
    profile = models.ForeignKey(UserProfile, related_name="occupation")
    responsibility = models.ForeignKey(Responsibility)
    company = models.CharField(max_length=60, blank=False)
    date_begin = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.responsibility