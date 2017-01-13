from django.forms.utils import flatatt
from django.forms.widgets import TextInput, Input
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class InputMaterial(Input):

    errors = None
    show_errors = True
    label = None

    def __init__(self, attrs=None):
        super(InputMaterial, self).__init__(attrs)

    @property
    def template(self):
        raise NotImplementedError("You must specify a 'template' property!")

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            final_attrs['value'] = force_text(self.format_value(value))
        if 'class' not in final_attrs:
            final_attrs['class'] = force_text(self.format_value('customform-input'))

        flatattrs = flatatt(final_attrs)

        return mark_safe(render(None, template_name=self.template, context={ 'self': self,
                                                                         'value': value,
                                                                         'flatattrs': flatattrs,
                                                                          'label': self.label,
                                                                         'attrs': final_attrs,
                                                                         'errors': self.errors if self.show_errors else None
                                                                        }).content)

class InputTextMaterial(InputMaterial):

    template = 'custom_base/input-text-material.html'
    input_type = 'text'

    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(InputTextMaterial, self).__init__(attrs)

class TextAreaMaterial(InputMaterial):

    template = 'custom_base/textarea-material.html'

