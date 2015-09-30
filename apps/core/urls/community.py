from django.conf.urls import url
from ..views.community import views, CoreCommunityFollowersView, CoreCommunityAboutView, CoreCommunityFeedView, CoreCommunityQuestionFeedView, CoreCommunitySearch, CoreCommunityList, \
    CoreCommunityQuestionList, CoreCommunityQuestionSearch

urlpatterns = [

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreCommunityFeedView.as_view(), name='show'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/about/$', CoreCommunityAboutView.as_view(), name='about'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', CoreCommunityFollowersView.as_view(), name='followers'),

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/search/$', CoreCommunitySearch.as_view(), name='search'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/list/$', CoreCommunityList.as_view(), name='list'),

    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/$', CoreCommunityQuestionFeedView.as_view(), name='questions'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/search/$', CoreCommunityQuestionSearch.as_view(), name='questions-search'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/list/$', CoreCommunityQuestionList.as_view(), name='questions-list'),

    ]