from django.contrib.auth import get_user_model
from django.db.models import Q
from django_thumbor import generate_url
from push_notifications.models import GCMDevice
from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.custom_base.service.custom import forms,  IdeiaForm
from apps.custom_base.widgets.material import InputTextMaterial
from apps.socialactions.models import UserAction
from apps.socialactions.service.business import get_by_label
from apps.userprofile.models import Responsibility


class SearchNotificationSubscribe(IdeiaForm):

    q = forms.CharField(required=False)
    communities = forms.ModelMultipleChoiceField(queryset=Community.objects.all(), required=False)
    responsibility = forms.ModelMultipleChoiceField(Responsibility.objects.all(), required=False)


    def __has_search_field(self, key):
        if key in self.cleaned_data and self.cleaned_data[key] is not None and self.cleaned_data[key] != '':
            return self.cleaned_data[key]
        else:
            return False

    def _get_queryset(self):
        q = self.__has_search_field("q")
        communities = self.__has_search_field("communities")
        responsibility = self.__has_search_field("responsibility")

        queryset = GCMDevice.objects.filter(active=True)

        if q:
            queryset = queryset.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q))

        if communities:
            communities_id = [community.id for community in communities]

            user_action_queryset = UserAction.objects.filter(
                    content_type=ContentTypeCached.objects.get(model='community'),
                    object_id__in=communities_id,
                    action_type=get_by_label('follow')
                ).prefetch_related("author").only("author")


            users_id = [item.author.id for item in user_action_queryset]
            user_queryset = get_user_model().objects.filter(id__in=users_id)
            queryset = queryset.filter(user__in=user_queryset)


        if responsibility:
            queryset = queryset.filter(user__profile__occupation__responsibility__in=responsibility)

        return queryset



    def __process__(self):
        return self._get_queryset().count()



class NotificationSend(SearchNotificationSubscribe):

    title = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)
    url = forms.URLField(required=True)


    def __process__(self):
        queryset = self._get_queryset()

        title = self.cleaned_data['title']
        message = self.cleaned_data['message']
        url = self.cleaned_data['url']

        icon_url = "https://www.portalgsti.com.br/static/images/favicon-96x96.png"
        icon_url = generate_url(icon_url, width=60, height=60)
        queryset.send_message(message, title=title, extra={'click_action': url, "icon": icon_url})

        return queryset


