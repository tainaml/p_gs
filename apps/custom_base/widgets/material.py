from __future__ import unicode_literals
from django.forms.utils import flatatt
from django.forms.widgets import Input, Select, CheckboxInput, CheckboxSelectMultiple, SelectMultiple
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class InputMaterial(Input):

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

    def render_options(self, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

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

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, extra_attrs={"type": self.input_type, "name": name})
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

class MaterialSelectMultiple(InputMaterial, SelectMultiple):

    _empty_value = []


    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)

    def get_aditional_context(self, name, value, attrs=None):

        return {'choices': self.choices}

    template = 'custom_base/selectize-material.html'

    def render(self, name, value, attrs=None, renderer=None):

        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, extra_attrs={"name": name})

        options = self.render_options(value)
        if 'class' not in final_attrs and self.class_name:
            final_attrs['class'] = force_text(self.format_value(self.class_name))
        flatattrs = flatatt(final_attrs)
        base_context={ 'self': self,
                             'value': value,
                             'flatattrs': flatattrs,
                              'options': options,
                              'label': self.label,
                             'attrs': final_attrs,
                             'errors': self.errors if self.show_errors else None
                            }
        base_context.update(self.get_aditional_context(name=name, value=value, attrs=attrs))

        return mark_safe(render(None, template_name=self.template, context=base_context).content)


class CheckboxSelectMultipleMaterial(InputMaterial, SelectMultiple):

    _empty_value = []
    input_type = 'checkbox'
    def get_aditional_context(self, name, value, attrs=None):

        choices = []
        for key, value in self.choices:
            choices.append([force_text(key), value])
        return {'choices': choices}

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value= set(force_text(v) for v in value)
        return super(CheckboxSelectMultipleMaterial, self).render(name=name, value=value, attrs=attrs)


    def use_required_attribute(self, initial):
        # Don't use the 'required' attribute because browser validation would
        # require all checkboxes to be checked instead of at least one.
        return False


    template = 'custom_base/select-multiple-checkbox-material.html'

