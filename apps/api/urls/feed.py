from django.conf.urls import url
from ..views import feed

urlpatterns = [
    url(r'^$', feed.FeedViewset.as_view({
        'get': 'list'
    }), name='list'),
    url(r'^(?P<pk>\d+)/$', feed.FeedViewset.as_view(
        {
            'get': 'retrieve'
        }
    ), name='retrieve'),


]