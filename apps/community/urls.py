from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', views.CommunityView.as_view(), name='show'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', views.CommunityFollowersView.as_view(), name='followers'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/about/$', views.CommunityAboutView.as_view(), name='about'),
]