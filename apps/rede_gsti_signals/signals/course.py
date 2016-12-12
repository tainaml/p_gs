import json
import urllib
import urllib2
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from apps.core.models.course import Course
from django.conf import settings

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

@receiver(post_save, sender=Course)
def course_created(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    if instance.class_link:
        post_save.disconnect(course_created, sender=Course)
        querystring = {
            'url': instance.class_link
        }

        url = reverse('core:oembed') +"?%s" % urllib.urlencode(encoded_dict(querystring))

        content = urllib2.urlopen(settings.SITE_URL+url).read()
        dict_content = json.loads(content)

        instance.embed = dict_content['html']
        instance.save()
        post_save.connect(course_created, sender=Course)


post_save.connect(course_created, sender=Course)



