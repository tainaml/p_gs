import json
from django.forms.utils import flatatt
from django.conf import settings
from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from ideia_summernote.widget import SummernoteWidget


class AdminSummernoteWidget(SummernoteWidget):

    def _media(self):
        django_jquery_adapter = settings.STATIC_URL + 'js/django-jquery-adapter.js'
        js = (django_jquery_adapter,) + self.assets.get('js')
        if self.load_init:
            js+= (settings.STATIC_URL + 'javascripts/summernote-init.js',)
        return forms.Media(css=self.assets.get('css'),
                           js=js)

    media = property(_media)

    # Override
    def render(self, name, value, attrs=None):

        if not attrs:
            attrs = {}

        attrs['data-toggle'] = "editor"
        attrs['config'] = json.dumps(self.editor_conf)

        if self.async:
            attrs['data-toggle'] = attrs['data-toggle'] + "async"

        final_attrs = self.build_attrs(attrs, name=name)

        return format_html('<textarea{}>\r\n{}</textarea>', flatatt(final_attrs), force_text(value))