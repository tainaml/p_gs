__author__ = 'phillip'
from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
from django.template.defaultfilters import slugify
import os

def plataform_image_upload(instance, filename):

    owner = instance.author.id
    today_str = datetime.today().strftime('%Y/%m/%d')
    path = 'plataform/{0}/{1}'.format(owner, today_str)

    ext = filename.split('.')[-1]
    name = slugify(".".join(filename.split('.')[0:-1]))
    return os.path.join(path, "{0}.{1}".format(name, ext))

class Plataform(models.Model):

    slug = models.SlugField(null=False, max_length=255, verbose_name=_('Slug'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))

    image = models.ImageField(max_length=100, upload_to=plataform_image_upload, blank=True)