import django.templatetags.static as default_static
from django import template
import json
from django.conf import settings
register = template.Library()
import os

class StaticVersionedNode(default_static.StaticNode):

    STATIC_JSON = 'rev-manifest.json'
    _VERSIONED_DICT = {}

    @staticmethod
    def versioned_dict():
        if not StaticVersionedNode._VERSIONED_DICT:
            with open(os.path.join(settings.BASE_DIR, 'static', StaticVersionedNode.STATIC_JSON)) as json_file:
                dict_file = json.load(json_file)
                for key in dict_file:
                    StaticVersionedNode._VERSIONED_DICT[os.path.join(settings.STATIC_URL, key)] = os.path.join(settings.STATIC_URL, dict_file[key])

        return StaticVersionedNode._VERSIONED_DICT

    @classmethod
    def handle_simple(cls, path):
        url = super(StaticVersionedNode, cls).handle_simple(path)
        if settings.DEBUG is True:
            return url
        return StaticVersionedNode.versioned_dict()[url]


@register.tag('static_versioned')
def do_static(parser, token):

    return StaticVersionedNode.handle_token(parser, token)

def static_versioned(path):

    return StaticVersionedNode.handle_simple(path)