from django.forms.utils import flatatt
from django.forms.widgets import Input, Select
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

    def get_aditional_context(self, name, value, attrs=None):
        return {}

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            final_attrs['value'] = force_text(self.format_value(value))
        if 'class' not in final_attrs:
            final_attrs['class'] = force_text(self.format_value('customform-input'))

        flatattrs = flatatt(final_attrs)
        base_context={ 'self': self,
                             'value': value,
                             'flatattrs': flatattrs,
                              'label': self.label,
                             'attrs': final_attrs,
                             'errors': self.errors if self.show_errors else None
                            }
        base_context.update(self.get_aditional_context(name=name, value=value, attrs=attrs))

        return mark_safe(render(None, template_name=self.template, context=base_context).content)

class InputTextMaterial(InputMaterial):

    template = 'custom_base/input-text-material.html'
    input_type = 'text'

    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(InputTextMaterial, self).__init__(attrs)

class URLMaterial(InputTextMaterial):

    input_type = 'url'

class EmailMaterial(InputTextMaterial):

    input_type = 'email'


class TextAreaMaterial(InputMaterial):

    template = 'custom_base/textarea-material.html'



class SelectMaterial(InputMaterial, Select):

    def get_aditional_context(self, name, value, attrs=None):
        return {'options': self.render_options([value])}

    template = 'custom_base/select-material.html'

