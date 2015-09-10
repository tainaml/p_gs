from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _


class GenderType():
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
    user = models.OneToOneField(User)
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    profile_picture = models.ImageField(max_length=100, upload_to='userprofile/%Y/%m/%d', blank=True, default='')

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

    def has_age(self):
        if self.birth:
            return True

    def age(self):
        if self.has_age:
            born = self.birth
            today = date.today()

            # return int(round((date.today() - self.birth).days / 365.2425, 3))
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def has_occupation(self):
        return True if self.occupation_set.all() else False

    def occupations(self):
        return self.occupation_set.all().order_by('-id')[0] if self.has_occupation() else None


class Occupation(models.Model):
    profile = models.ForeignKey(UserProfile)
    responsibility = models.CharField(max_length=60, blank=False)
    company = models.CharField(max_length=60, blank=False)
    date_begin = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.responsibility