from django.forms.utils import flatatt
from django.forms.widgets import Input, Select, CheckboxInput, CheckboxSelectMultiple
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class InputMaterial(Input):

    errors = None
    show_errors = True
    label = None
    class_name = 'customform-input'

    def __init__(self, attrs=None):
        super(InputMaterial, self).__init__(attrs)

    @property
    def template(self):
        raise NotImplementedError("You must specify a 'template' property!")

    def get_aditional_context(self, name, value, attrs=None):
        return {}

    def get_aditional_attrs(self, name, value, attrs=None):
        aditional_attrs = {}
        if value != '':
            aditional_attrs['value'] = force_text(self.format_value(value))
        return aditional_attrs

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs.update(self.get_aditional_attrs(name=name, value=value, attrs=attrs))

        if 'class' not in final_attrs and self.class_name:
            final_attrs['class'] = force_text(self.format_value(self.class_name))

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

class NumberMaterial(InputTextMaterial):

    input_type = 'number'

class BooleanMaterial(InputTextMaterial, CheckboxInput):

    input_type = 'checkbox'
    template = 'custom_base/input-boolean-material.html'
    class_name = None


    def get_aditional_attrs(self, name, value, attrs=None):
        aditional_attrs = {}

        #Django's code
        if self.check_test(value):
            aditional_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            aditional_attrs['value'] = force_text(value)


        return aditional_attrs


class TextAreaMaterial(InputMaterial):

    template = 'custom_base/textarea-material.html'



class SelectMaterial(InputMaterial, Select):
    
    def get_aditional_context(self, name, value, attrs=None):
        return {'options': self.render_options([value])}

    template = 'custom_base/select-material.html'


class CheckboxSelectMultipleMaterial(InputMaterial):
    input_type = 'checkbox'
    def get_aditional_context(self, name, value, attrs=None):

        return {'choices': self.choices}


    def use_required_attribute(self, initial):
        # Don't use the 'required' attribute because browser validation would
        # require all checkboxes to be checked instead of at least one.
        return False


    template = 'custom_base/select-multiple-checkbox-material.html'

