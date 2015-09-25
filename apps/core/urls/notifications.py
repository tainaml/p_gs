from django.conf.urls import url
from ..views.notifications import CoreNotificationIndexView, CoreNotificationMembersView

urlpatterns = [
    url(r'^/$', CoreNotificationIndexView.as_view(), name='index'),
    url(r'^members/$', CoreNotificationMembersView.as_view(), name='members')
]