__author__ = 'phillip'

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^act/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)', views.SocialActionView.as_view(), name='act'),
    url(r'^act/xhr/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)', views.SocialActXHR.as_view(), name='act-xhr'),
    url(r'^acted/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)', views.SocialUserActed.as_view(), name='acted'),

    url(r'^act/ajax/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)', views.SocialActionAjax.as_view(), name='act-ajax'),
    url(r'^act/suggest/(?P<object_to_link>[0-9]+)/(?P<content>[a-z]+)/$', views.SocialActionSuggestArticleToUser.as_view(), name='act-suggest'),
    url(r'^followers/(?P<content_type_id>[0-9]+)/(?P<object_filter_id>[0-9]+)/$', views.SocialActionFollowersViews.as_view(), name='get_followers'),
    url(r'^followings/(?P<content_type_id>[0-9]+)/(?P<object_filter_id>[0-9]+)/$', views.SocialActionFollowingsViews.as_view(), name='get_followings'),

]