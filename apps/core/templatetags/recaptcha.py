from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag()
def recaptcha_site_key():
    return settings.NORECAPTCHA_SITE_KEY
