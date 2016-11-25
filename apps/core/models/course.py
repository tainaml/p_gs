from django.utils.functional import cached_property
from apps.core.models.languages import Language
from apps.taxonomy.models import Taxonomy

__author__ = 'phillip'

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
from django.template.defaultfilters import slugify
import os

def course_image_upload(instance, filename):

    owner = instance.author.id
    today_str = datetime.today().strftime('%Y/%m/%d')
    path = 'course/{0}/{1}'.format(owner, today_str)

    ext = filename.split('.')[-1]
    name = slugify(".".join(filename.split('.')[0:-1]))
    return os.path.join(path, "{0}.{1}".format(name, ext))

class Course(models.Model):

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('Rating'))

    internal_author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='courses',
                               verbose_name=_('Internal author'))

    external_author = models.TextField(max_length=255, verbose_name=_('External Author'))

    @cached_property
    def author(self):
        return self.internal_author or self.external_author


    def image_or_default(self):
        #TODO
        return self.image or None

    updatein = models.DateTimeField(null=False, auto_now=True)
    curriculum = models.TextField(max_length=255, verbose_name=_('Curriculum'))

    languages = models.ManyToManyField(Language, blank=True, verbose_name=_('Languages'), related_name="languages")
    image = models.ImageField(max_length=100, upload_to=course_image_upload, blank=True, verbose_name=_('Image'))
    related_courses = models.ManyToManyField("self", blank=True, verbose_name=_('Related Courses'))
    taxonomies = models.ManyToManyField(Taxonomy, blank=True, verbose_name=_('Taxonomy'), related_name="taxonomies")

    affiliate_link = models.URLField(verbose_name=_('Affiliate link'))



