from django.db import models

class Tags(models.Model):

    tag_name = models.CharField(null=False, max_length=100)
    tag_slug = models.SlugField(null=False, max_length=150)
    tag_order = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return self.tag_name

    def save(self, *args, **kwargs):
        return super(Tags, self).save(*args, **kwargs)