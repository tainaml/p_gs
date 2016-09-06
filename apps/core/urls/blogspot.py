from django.conf.urls import url
from ..views.search import SearchAll

urlpatterns = [
    url(r'search/label/(?P<params>.*)$', SearchAll.as_view(), name='label-search'),
]