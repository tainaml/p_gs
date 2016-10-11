from django import template
import bleach
from django.conf import settings
import re
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

register = template.Library()


class AmpHtmlParser(HTMLParser):
    pass


@register.simple_tag(takes_context=True)
def amp_normalize_text(context, text):

    ALLOWED_TAGS = [
        'p', 'img', 'video', 'audio', 'iframe',
        'button', 'a', 'svg', 'ul', 'li', 'ol'
    ]

    attrs = {
        '*': [],
        'img': ['src'],
        'iframe': ['src']
    }

    styles = []

    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=attrs,
        styles=styles,
        strip=True
    )

    cleaned = re.sub(
        '(<img).+(src="(?P<image_src>/media/uploads(.*)))"',
        r'<img \2 src=\"{}\3\"'.format(''),
        cleaned
    )
    cleaned = re.sub('(\<img)', r'<amp-img layout="responsive" height="320px" width="320px" ', cleaned)
    # cleaned = re.sub('\<iframe', '<amp-iframe layout="responsive" sandbox="allow-scripts" ', cleaned)

    return cleaned
