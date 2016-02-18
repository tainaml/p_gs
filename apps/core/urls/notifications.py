from django.conf.urls import url

from ..views import notifications as core_view

urlpatterns = [

    url(r'^$', core_view.CoreNotificationIndexView.as_view(), name='index'),
    url(r'^members$', core_view.views.NotificationMembersView.as_view(), name='members'),
    url(r'^posts$', core_view.views.NotificationPostsView.as_view(), name='posts'),
    url(r'^general$', core_view.views.NotificationGeneralsView.as_view(), name='general'),

    url(r'^mark-as-read', core_view.views.NotificationMarkAsRead.as_view(), name='mark-as-read'),
    url(r'^mark-as-visualized', core_view.views.NotificationMarkAsVisualized.as_view(), name='mark-as-visualized'),

    url(r'^clear$', core_view.CoreNotificationClear.as_view(), name='clear'),
    url(r'^poll/count/(?P<notification_type>[a-z]+)$', core_view.CoreNotificationPollingCount.as_view(),
        name='polling-count'),
    url(r'^poll/load/(?P<notification_type>[a-z]+)$', core_view.CoreNotificationPollingLoad.as_view(),
        name='polling-load')

]
