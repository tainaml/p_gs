from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views import notifications as core_view

urlpatterns = [

    url(_(r'^$'), core_view.CoreNotificationIndexView.as_view(), name='index'),
    url(_(r'^members$'), core_view.views.NotificationMembersView.as_view(), name='members'),
    url(_(r'^posts$'), core_view.views.NotificationPostsView.as_view(), name='posts'),
    url(_(r'^general$'), core_view.views.NotificationGeneralsView.as_view(), name='general'),

    url(_(r'^mark-as-read$'), core_view.CoreNotificationMarkAsRead.as_view(), name='notification-as-read'),
    url(_(r'^mark-all-as-read$'), core_view.views.NotificationMarkAllAsRead.as_view(), name='mark-as-read'),
    url(_(r'^mark-as-read-visualized$'), core_view.CoreNotificationMarkAsReadAndVisualized.as_view(), name='mark-as-read-and-visualized'),
    url(_(r'^mark-all-as-visualized$'), core_view.views.NotificationMarkAllAsVisualized.as_view(), name='mark-as-visualized'),

    url(_(r'^clear$'), core_view.CoreNotificationClear.as_view(), name='clear'),
    url(_(r'^poll/count/(?P<notification_type>[a-z]+)$'), core_view.CoreNotificationPollingCount.as_view(),
        name='polling-count'),
    url(_(r'^poll/load/(?P<notification_type>[a-z]+)$'), core_view.CoreNotificationPollingLoad.as_view(),
        name='polling-load')

]
