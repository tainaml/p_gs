from django.conf.urls import url
from apps.core.views import socialactions

urlpatterns = [

    url(r'^filter/followings/$', socialactions.SocialActionFilterFollowings.as_view(), name='filter_followings'),
    url(r'^counter-actions/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/(?P<action>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', socialactions.CountActions.as_view(), name='counter-actions'),

]
