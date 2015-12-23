from django.conf import settings
from django.core.exceptions import ValidationError
from custom_forms.custom import forms, IdeiaForm
import business as notification_business
__author__ = 'phillip'


class ListNotificationForm(IdeiaForm):

    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, user=None, notification_actions=None, itens_by_page=10, *args, **kwargs):
        if not notification_actions:
            notification_action = []
        self.notification_actions = notification_actions
        self.itens_by_page = itens_by_page
        self.user= user
        super(ListNotificationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ListNotificationForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):

        return notification_business.get_notifications_by_user_and_notification_type_list(
            user=self.user,
            notification_actions=self.notification_actions,
            items_per_page=self.itens_by_page,
            page=self.cleaned_data['page']
        )


