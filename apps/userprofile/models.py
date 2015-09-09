from django.db import models
from django.contrib.auth.models import User
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


class Occupation(models.Model):

    responsibility = models.CharField(max_length=60, blank=False)
    description = models.TextField(blank=False)
    profile = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.responsibility