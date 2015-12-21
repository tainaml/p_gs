from django.conf.urls import url
from ..views import notifications as core_view

urlpatterns = [
    url(r'^/$', core_view.CoreNotificationIndexView.as_view(), name='index'),
    url(r'^members/$', core_view.CoreNotificationMembersView.as_view(), name='members'),

    url(r'^poll/count/(?P<notification_type>[a-z]+)$', core_view.CoreNotificationPollingCount.as_view(), name='polling-cpunt')
]