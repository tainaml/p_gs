from django.db import models
from django.contrib.auth.models import User


class GenderType():

    def __init__(self):
        pass

    MALE = 'M'
    FEMALE = 'F'


class Country(models.Model):

    name = models.CharField(max_length=60, blank=False)
    abbreviation = models.CharField(max_length=3, blank=False)

    def __str__(self):
        return self.name


class State(models.Model):

    name = models.CharField(max_length=60, blank=False)
    abbreviation = models.CharField(max_length=3, blank=False)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name


class City(models.Model):

    name = models.CharField(max_length=60, blank=False)
    state = models.ForeignKey(State)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    birth = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=1, default=None, null=True)
    city = models.ForeignKey(City)

    def __str__(self):
        return self.user


class Occupation(models.Model):

    responsibility = models.CharField(max_length=60, blank=False)
    description = models.TextField(blank=False)
    user = models.ForeignKey(User)