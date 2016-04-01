from datetime import date

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _

from ckeditor.fields import RichTextField

from apps.account.models import User
from apps.socialactions.models import Counter
from apps.geography.models import State, City, Country


class GenderType:
    def __init__(self):
        pass

    MALE = 'M'
    FEMALE = 'F'

    LABEL = {
        MALE: _("MALE"),
        FEMALE: _("FEMALE")
    }


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, related_name='profiles_city')
    city_hometown = models.ForeignKey(City, null=True, blank=True, related_name='profiles_city_hometown')
    profile_picture = models.ImageField(max_length=100, upload_to='userprofile/%Y/%m/%d', blank=True, default='')
    contributor = models.BooleanField(null=False, blank=False, default=False)
    wizard_step = models.IntegerField(null=False, blank=False, default=0)

    def __unicode__(self):
        return self.user.get_full_name()

    def has_locale_living(self):
        if self.city and self.city.state and self.city.state.country:
            return True
        return False

    def locale(self):
        if self.has_locale_living():
            return "%s - %s - %s" % (self.city.name.title(),
                                     self.city.state.acronym.upper(),
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

    # User Action Follower
    @property
    def followers(self):
        try:
            return Counter.objects.defer("count").get(
                action_type=settings.SOCIAL_FOLLOW,
                object_id=self.id,
                content_type= ContentType.objects.get(model='community')

            ).count
        except:
            return 0

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

    def isContributor(self):
        return self.contributor is True


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
        return self.responsibility.name
