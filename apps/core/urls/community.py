from django.conf.urls import url
from ..views.community import views, CoreCommunityView, CoreCommunityFollowersView, CoreCommunityAboutView

urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreCommunityView.as_view(), name='show'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', CoreCommunityFollowersView.as_view(), name='followers'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/about/$', CoreCommunityAboutView.as_view(), name='about'),
    ]