from django.db import models


class Community(models.Model):

    title = models.CharField(blank=False, null=False, max_length=100)
    slug = models.SlugField(blank=False, null=False, max_length=150)
    description = models.TextField(null=False, max_length=2048)
    image = models.ImageField(max_length=100, upload_to='community/%Y/%m/%d', blank=True, default='')

    def __unicode__(self):
        return self.title

    def get_picture(self):
        return self.image if self.image else None