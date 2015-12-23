from django.conf.urls import url
from ..views.notifications import CoreNotificationIndexView, CoreNotificationMembersView, CoreNotificationListView, \
    CoreNotificationMemberListView

urlpatterns = [
    url(r'^/$', CoreNotificationIndexView.as_view(), name='index'),
    url(r'^list/members$', CoreNotificationMemberListView.as_view(), name='list-members'),
    # url(r'^list/members$', CoreAnswersAndCommentsListView.as_view(), name='list-members'),
    # url(r'^list/members$', CoreGeneralListView.as_view(), name='list-members'),
    url(r'^members/$', CoreNotificationMembersView.as_view(), name='members')
]