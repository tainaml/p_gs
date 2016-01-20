from custom_forms.custom import IdeiaForm, forms
from ..business import configuration as BusinessConfig


class ConfigNotificationsForm(IdeiaForm):
    NOTIFY_PUBLICATIONS_CHOICES = (
        ('all', 'All'),
        ('articles', 'Articles'),
        ('questions', 'Questions')
    )

    notify_follow = forms.BooleanField(required=False, initial=True)
    notify_comment_article = forms.BooleanField(required=False, initial=True)
    notify_comment_question = forms.BooleanField(required=False, initial=True)

    notify_publications = forms.ChoiceField(required=True, choices=NOTIFY_PUBLICATIONS_CHOICES)

    def __init__(self, *args, **kwargs):
        self.entity = None

        super(ConfigNotificationsForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super(ConfigNotificationsForm, self).is_valid()
        return is_valid

    def set_entity(self, entity):
        self.entity = entity

    def __process__(self):
        return BusinessConfig.save_configs(
            self.entity,
            self.cleaned_data
        )
