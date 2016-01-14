from django.conf.urls import url

from apps.core.views import configuration as CoreView

urlpatterns = [

    url(r'^account$', CoreView.CoreSettingsAccountView.as_view(), name='account'),
    url(r'^notification$', CoreView.CoreSettingsNotificationView.as_view(), name='notification'),

]