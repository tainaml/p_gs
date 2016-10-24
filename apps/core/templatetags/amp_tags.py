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
        'button', 'a', 'svg', 'ul', 'li', 'ol',
        'strike', 'b', 'i', 'hr',
        'pre', 'code', 'blockquote',
        'table', 'tbody', 'tr', 'td',
        'h2', 'h3', 'h4', 'h5'
    ]

    attrs = {
        '*': [],
        'img': ['src'],
        'iframe': ['src'],
        'a': ['href'],
        'code': ['class'],
        'span': ['class'],
    }

    styles = [
        'text-align'
    ]

    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=attrs,
        styles=styles,
        strip=True
    )

    # cleaned = re.sub(
    #     '(<img).+(src="(?P<image_src>/media/uploads(.*)))"',
    #     r'<img \2 src=\"{}\3\"'.format(''),
    #     cleaned
    # )

    cleaned = re.sub('<iframe', '<amp-iframe layout="responsive" sandbox="allow-scripts allow-same-origin" height="212" width="320" ', cleaned)
    cleaned = re.sub('</iframe>', '</amp-iframe>', cleaned)

    cleaned = re.sub('(\<img )', r'<amp-img layout="responsive" height="200" width="320" ', cleaned)

    return cleaned
