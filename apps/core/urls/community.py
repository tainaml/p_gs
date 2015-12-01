from django.conf.urls import url
from ..views import community as CoreViews

urlpatterns = [

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreViews.CoreCommunityFeedView.as_view(), name='show'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/about/$', CoreViews.CoreCommunityAboutView.as_view(), name='about'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', CoreViews.CoreCommunityFollowersView.as_view(), name='followers'),

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/search/$', CoreViews.CoreCommunitySearch.as_view(), name='search'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/list/$', CoreViews.CoreCommunityList.as_view(), name='list'),

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/$', CoreViews.CoreCommunityQuestionFeedView.as_view(), name='questions'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/search/$', CoreViews.CoreCommunityQuestionSearch.as_view(), name='questions-search'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/list/$', CoreViews.CoreCommunityQuestionList.as_view(), name='questions-list'),

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/$', CoreViews.CoreCommunityVideosView.as_view(), name='videos'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/$', CoreViews.CoreCommunityVideosSearch.as_view(), name='videos-search'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/list/$', CoreViews.CoreCommunityVideosList.as_view(), name='videos-list'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/related/$', CoreViews.CommunityRelated.as_view(), name='related'),

    url(r'^load/async/(?P<object_id>[0-9]+)/(?P<content_type>[a-z]+)/$', CoreViews.CoreCommunityLoad.as_view(), name='load-communities-async'),
    url(r'^search/followers$', CoreViews.CoreCommunityFollowersSearch.as_view(), name='search-followers'),
    url(r'^search/followers/list$', CoreViews.CoreCommunityFollowersSearchList.as_view(), name='search-followers-list'),

]