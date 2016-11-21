from django.forms.widgets import Widget, Select
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class SelectizeSelectSingle(Select):

    class Media:

        css = {
            'all': ('selectize/selectize.css', 'selectize/main.css')
        }

        js = ('selectize/selectize.min.js', 'selectize/main.js')

    def render(self, name, value, attrs=None):

        attrs = attrs if attrs else {}

        classes = attrs.get('class', '').split(' ')

        classes.append('testejr')

        attrs.update({
            'data-ideia-selectize': True
        })

        final_attrs = self.build_attrs(attrs, name=name)

        output = [format_html('<select{}>', flatatt(final_attrs))]
        output.append('</select>')

        return mark_safe('\n'.join(output))