from django.forms import widgets
from django.utils.html import format_html
from django.utils.safestring import mark_safe

IDEIA_AVAIABLE_FIELDS = [
    widgets.TextInput, widgets.Textarea, widgets.Select,
    widgets.EmailInput, widgets.URLInput, widgets.Input, widgets.NumberInput,
    widgets.PasswordInput,
]

def ideia_field_wraper(field):

    try:

        widget_class = field.widget.__class__
        if widget_class in IDEIA_AVAIABLE_FIELDS:

            field.custom_label = field.label if field.label else ''
            field.label = ''

            widget = field.widget
            widget.render = ideia_wrapper_render(widget.render, field)
        return field
    except Exception as e:
        print(e)
        return field


def ideia_wrapper_render(render_func, field=None, label=None):

    def render_label(name, label, active=''):
        return mark_safe(u'<label class="customform-label {active}" for="{name}">{label_html}</label>'.format(
            name=name,
            label_html=label,
            active=active
        ))

    def render(name, value, attrs=None):

        label_html = ''

        attrs.update({
            'class': '{} {}'.format('customform-input', attrs.get('class', ''))
        })

        if value:
            attrs.update({
                'class': '{} {}'.format(attrs.get('class', ''), 'active')
            })

        active_class = 'active' if value else ''

        if field and field.custom_label:

            label_html = render_label(name, field.custom_label, active=active_class)

        if label:
            label_html = render_label(name, label, active=active_class)

        new_html = u'<div class="customform">\r\n{widget}\r\n<hr>{label}</div>'.format(
            widget=render_func(name, value, attrs),
            label=label_html
        )

        return mark_safe(new_html)

    return render

def ideia_custom_fielder(class_name='custom_form'):

    def wrapper(form_cls):

        for field in form_cls.base_fields.itervalues():
            ideia_field_wraper(field)

        return form_cls

    return wrapper


class CustomFielderWidget(object):

    @staticmethod
    def factory(widget, label=None):

        class new_widget(widget):

            def __init__(self, *args, **kwargs):
                super(new_widget, self).__init__(*args, **kwargs)
                self.old_render = self.render
                self.render = ideia_wrapper_render(self.old_render, field=None)

        return new_widget