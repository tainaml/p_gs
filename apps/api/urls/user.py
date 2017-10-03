from django.conf.urls import url
from ..views import user

urlpatterns = [
    url(r'^(?P<pk>\d+|current+)/$', user.UserViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    ), name='retrieve'),
    url(r'^$', user.UserViewSet.as_view({'get': 'list'}), name='list'),


]