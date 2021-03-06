from django import forms
from django.db import transaction
from ideia_summernote.widget import SummernoteWidget
from models import UserAlert
from apps.notifications.service import business as Business
from django.contrib.auth import get_user_model
from django.conf import settings

class UserAlertForm(forms.ModelForm):

    @transaction.atomic
    def save(self, commit=True):
        instance = super(UserAlertForm, self).save(commit=commit)

        if instance.status == UserAlert.STATUS_PUBLISH:
            author_id = getattr(settings, 'NOTIFICATION_ALERT_DEFAULT_AUTHOR')
            UserModel = get_user_model()
            author = UserModel.objects.get(id=author_id)

            Business.send_notification_to_many(
                author=author,
                to_list=instance.users.all(),
                target_object=instance,
                notification_action=getattr(settings, 'NOTIFICATION_USERALERT')
            )
            instance.status = UserAlert.STATUS_SENDED
            instance.save()


        return instance




    class Meta:
        model = UserAlert
        exclude = ()
        widgets = {
            'content': SummernoteWidget(editor_conf='article')
        }