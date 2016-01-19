from custom_forms.custom import forms, IdeiaForm
import business as Business


class NotificationForm(IdeiaForm):
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, items_per_page=10, *args, **kwargs):
        self.notification_actions = None
        self.items_per_page = items_per_page
        self.user = None
        self.read = None

        super(NotificationForm, self).__init__(*args, **kwargs)

    def set_to_user(self, user):
        self.user = user

    def set_notification_group(self, notification_group):
        self.notification_actions = notification_group

    def set_read(self, read):
        self.read = read

    def clean(self):
        cleaned_data = super(NotificationForm, self).clean()
        cleaned_data['page'] = cleaned_data.get('page', 1)

        return cleaned_data

    def __process__(self):
        return Business.get_notifications(
            self.user,
            self.notification_actions,
            self.read,
            self.items_per_page,
            self.cleaned_data.get('page')
        )
