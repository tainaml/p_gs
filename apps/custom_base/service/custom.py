from django import forms
import logging
from django.forms import widgets
from apps.custom_base.widgets.material import InputTextMaterial, TextAreaMaterial, SelectMaterial, URLMaterial, \
    EmailMaterial, NumberMaterial, BooleanMaterial

logger = logging.getLogger('error')

class AbstractIdeiaForm(object):
    def process(self):
        # :try:
        return self.__process__() if self.is_valid() else False
        # except NotImplementedError:
        #     raise NotImplementedError
        # except Exception, e:
        #     if settings.DEBUG:
        #         raise e
        #     else:
        #         logger.error(e)
        #         self.add_error(None, "General error!")
        #         return False

    def __process__(self):
        raise NotImplementedError

    def is_valid(self):
        pass

    def add_error(self, *args, **kwargs):
        pass


class IdeiaForm(forms.Form, AbstractIdeiaForm):
    def __init__(self, *args, **kwargs):
        super(IdeiaForm, self).__init__(*args, **kwargs)


class IdeiaModelForm(forms.ModelForm, AbstractIdeiaForm):

    def __init__(self, *args, **kwargs):
        super(IdeiaModelForm, self).__init__(*args, **kwargs)

MATERIAL_WIDGETS = {
    widgets.TextInput: InputTextMaterial,
    widgets.Textarea: TextAreaMaterial,
    widgets.Select: SelectMaterial,
    widgets.URLInput: URLMaterial,
    widgets.EmailInput: EmailMaterial,
    widgets.NumberInput: NumberMaterial,
    widgets.CheckboxInput: BooleanMaterial,
}

class MaterialModelForm(forms.ModelForm):

    def __update_fields__(self, attrs=None):

        for key in self.fields:

            field = self.fields[key]
            widget = field.widget
            if (not self._meta.widgets or key not in self._meta.widgets) and  type(widget) in MATERIAL_WIDGETS:
                field.widget = MATERIAL_WIDGETS[type(widget)](attrs=attrs)
                field.widget.label = field.label
                if hasattr(field, "choices"):
                    field.widget.choices = field.choices

    def __init__(self, *args, **kwargs):
        super(MaterialModelForm, self).__init__(*args, **kwargs)
        attrs = kwargs.get('attrs')
        self.__update_fields__(attrs=attrs)

    def add_error(self, field, error):
        super(MaterialModelForm, self).add_error(field=field, error=error)
        self.__update_error__(field=field)


    def __update_error__(self, field):
        if field:
            widget = self.fields[field].widget

            if (not self._meta.widgets  or field and field not in self._meta.widgets) \
                    and type(widget) in MATERIAL_WIDGETS.values() and field in self.errors:
                    self.fields[field].widget.errors = self.errors[field]

    def is_valid(self):
        valid = super(MaterialModelForm, self).is_valid()
        for key in self.fields:
           self.__update_error__(field=key)

        return valid

