from django.forms import widgets
from django.utils.html import format_html
from django.utils.safestring import mark_safe

IDEIA_AVAIABLE_FIELDS = [
    widgets.TextInput, widgets.Textarea, widgets.Select,
    widgets.EmailInput, widgets.URLInput, widgets.Input, widgets.NumberInput,
    widgets.PasswordInput,
]

def ideia_wrapper_render(render_func, field):

    def render(name, value, attrs=None):

        label_html = ''

        attrs.update({
            'class': '{} {}'.format('customform-input', attrs.get('class', ''))
        })

        if field.custom_label:

            label_html = mark_safe(u'<label class="customform-label" for="{name}">{label_html}</label>'.format(
                name=name,
                label_html=field.custom_label
            ))

        new_html = u'<div class="customform">\r\n{widget}\r\n<hr>{label}</div>'.format(
            widget=render_func(name, value, attrs),
            label=label_html
        )

        return mark_safe(new_html)

    return render

def ideia_custom_fielder(class_name='custom_form'):

    def wrapper(form_cls):

        for field in form_cls.base_fields.itervalues():
            widget_class = field.widget.__class__
            if widget_class in IDEIA_AVAIABLE_FIELDS:

                field.custom_label = field.label if field.label else ''
                field.label = ''

                widget = field.widget
                widget.render = ideia_wrapper_render(widget.render, field)

        return form_cls

    return wrapper
