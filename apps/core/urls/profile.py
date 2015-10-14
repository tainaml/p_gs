from django.conf.urls import url
from apps.core.views.user import CoreUserFeed

urlpatterns = [

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/articles/search/$', CoreUserFeed.as_view(), name='userfeed-search'),
    ]