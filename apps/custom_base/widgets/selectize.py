from django.forms.widgets import Select
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from apps.core.views.selectize import register


class SelectizeSelectSingle(Select):

    class Media:

        css = {
            'all': ('selectize/selectize.css', 'selectize/main.css')
        }

        js = ('selectize/selectize.min.js', 'selectize/main.js')

    def __init__(self, unique_name, attrs=None, choices=(), search_fields=(), value_field='', label_field=''):
        super(SelectizeSelectSingle, self).__init__(attrs=attrs, choices=choices)
        self.unique_name = unique_name
        self.search_fields = search_fields
        self.label_field = label_field
        self.value_field = value_field

    def render(self, name, value, attrs=None):

        register.add_item(
            key=self.unique_name,
            queryset=self.choices.queryset,
            label_field=self.label_field,
            value_field=self.value_field,
            search_fields=self.search_fields,
        )

        attrs = attrs if attrs else {}

        classes = attrs.get('class', '').split(' ')

        attrs.update({
            'data-ideia-selectize': True,
            'class': classes,
            'data-value': value
        })

        final_attrs = self.build_attrs(attrs, name=name)

        output = [format_html('<select{}>', flatatt(final_attrs))]
        output.append('</select>')

        return mark_safe('\n'.join(output))