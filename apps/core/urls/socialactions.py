from django.conf.urls import url
from apps.core.views import socialactions

urlpatterns = [

    url(r'^filter/followings/$', socialactions.SocialActionFilterFollowings.as_view(), name='filter_followings'),

]

