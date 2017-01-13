from django import forms
import logging
from django.forms import widgets
from apps.custom_base.widgets.material import InputTextMaterial, TextAreaMaterial, SelectMaterial

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
    widgets.Select: SelectMaterial
}

class MaterialModelForm(forms.ModelForm):

    def __update_fields__(self, attrs=None):

        for key in self.fields:
            widget = self.fields[key].widget

            if key not in self._meta.widgets and type(widget) in MATERIAL_WIDGETS:

                self.fields[key].widget = MATERIAL_WIDGETS[type(widget)](attrs=attrs)
                self.fields[key].widget.label = self.fields[key].label


    def __init__(self, *args, **kwargs):
        super(MaterialModelForm, self).__init__(*args, **kwargs)
        attrs = kwargs.get('attrs')
        self.__update_fields__(attrs=attrs)


    def is_valid(self):
        valid = super(MaterialModelForm, self).is_valid()
        for key in self.fields:
            widget = self.fields[key].widget

            if key not in self._meta.widgets and type(widget) in MATERIAL_WIDGETS.values() and key in self.errors:
                self.fields[key].widget.errors = self.errors[key]

        return valid

