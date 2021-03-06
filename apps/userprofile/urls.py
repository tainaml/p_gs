from django.conf.urls import url

from . import views
from apps.core.views import user as userView

urlpatterns = [

    url(r'^edit/$', views.ProfileEditView.as_view(), name='edit'),

    url(r'^get_state/$', views.ProfileGetState.as_view(), name='get_state'),
    url(r'^get_city/$', views.ProfileGetCity.as_view(), name='get_city'),

    url(r'^occupation/$', views.OccupationManageView.as_view(), name='occupation_manage'),
    url(r'^occupation/add/$', views.OccupationAddView.as_view(), name='occupation_add'),
    url(r'^occupation/(?P<occupation_id>[0-9]+)/$', views.OccupationShowView.as_view(), name='occupation_show'),
    url(r'^occupation/edit/(?P<occupation_id>[0-9]+)/$', views.OccupationEditView.as_view(), name='occupation_edit'),
    url(r'^occupation/delete/(?P<occupation_id>[0-9]+)/$', views.OccupationDeleteView.as_view(), name='occupation_delete'),

    url(r'^feed/$', userView.CoreUserFeed.as_view(), name='user_feed'),
    url(r'^(?P<username>[a-z0-9_-]+)/$', userView.CoreUserProfile.as_view(), name='user_profile'),
    url(r'^search/(?P<username>[a-z0-9_-]+)/$', userView.CoreUserSearch.as_view(), name='search'),
    url(r'^list/(?P<username>[a-z0-9_-]+)/$', userView.CoreUserList.as_view(), name='list'),
    url(r'^list_articles/(?P<username>[a-z0-9_-]+)/$', userView.CoreUserList.as_view(), name='list_articles'),

    url(r'^(?P<username>[a-z0-9_-]+)/$', views.ProfileShowView.as_view(), name='show'),
    url(r'^(?P<username>[a-z0-9_-]+)/followings/$', views.ProfileFollowingsView.as_view(), name='followings'),
    url(r'^(?P<username>[a-z0-9_-]+)/followers/$', views.ProfileFollowersView.as_view(), name='followers'),
    url(r'^(?P<username>[a-z0-9_-]+)/communities/$', views.ProfileCommunitiesView.as_view(), name='communities'),

]